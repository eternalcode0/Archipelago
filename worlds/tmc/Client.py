from typing import TYPE_CHECKING, Set, Dict

import asyncio

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Locations import all_locations, LocationData, LOC_TYPE_GROUND
from .Items import items_by_id

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


ROM_ADDRS = {
    "game_identifier": (0xA0, 8, "ROM"),
}

RAM_ADDRS = {
    # 0x00: Gameplay
    # 0x01: File creation
    # 0x02: Language menu
    # 0x03: File options
    # 0x04: File select
    # 0x05: File copy
    # 0x06: File delete
    # 0x07: File load
    "game_state": (0x1002, 1, "IWRAM"),
    # The room id in the 1st byte, area id in the 2nd
    "room_area_id": (0x0BF4, 2, "IWRAM"),
    # 0x00 Denotes whether the player can input, 0x01 cannot input. Not to be confused with can move/interact.
    # Can still be set to 0x00 when the player is in confusing situations such as reading textboxes
    "link_control": (0x3F9A, 1, "IWRAM"),
    # 0x11: Standard gameplay
    # 0x12: Reading dialog?
    # 0x13: Growing (yes, there's a separate state for growing from minish and none for shrinking)
    # 0x16: Watching Cutscene
    "link_priority": (0x1171, 1, "IWRAM"),
    # An arbitrary address that isn't used strictly by the game
    # We'll use it to store the index of the last processed remote item
    "received_index": (0x3FE0E, 2, "EWRAM"),
    "vaati_address": (0x2CA6, 1, "EWRAM"),
}


class MinishCapClient(BizHawkClient):
    game = "The Minish Cap"
    system = "GBA"
    patch_suffix = ".aptmc"
    local_checked_locations: Set[int]
    location_name_to_id: Dict[str, int]
    location_by_room_area: Dict[int, [LocationData]]
    room: int

    def __init__(self) -> None:
        super().__init__()
        self.location_name_to_id = {loc_data.name: loc_data.ram_addr for loc_data in all_locations}
        self.local_checked_locations = set()
        self.location_by_room_area = {}
        self.room = 0x0000

        for loc in all_locations:
            if loc.roomArea in self.location_by_room_area:
                self.location_by_room_area[loc.roomArea].append(loc)
            else:
                self.location_by_room_area[loc.roomArea] = [loc]

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if rom_name != "GBAZELDA":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.25

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed:
            return

        try:
            # Handle giving the player items
            read_result = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_state"], # Current state of game (is the player actually in-game?)
                RAM_ADDRS["room_area_id"],
                RAM_ADDRS["link_control"],
                RAM_ADDRS["link_priority"],
                RAM_ADDRS["received_index"],
                RAM_ADDRS["vaati_address"],
            ])
            if read_result is None:
                return
            game_state = read_result[0][0]
            room_area_id = int.from_bytes(read_result[1], "little")
            link_control = read_result[2][0]
            link_priority = read_result[3][0]
            received_index = (read_result[4][0] << 8) + read_result[4][1]
            vaati_address = read_result[5][0]

            locs_to_send = set()

            # Check for goal, since vaati's defeat triggers a cutscene this has to be checked before the next if
            # specifically because it sets the game_state to 0x04
            if not ctx.finished_game and vaati_address | 0x02 == vaati_address:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

            # Early return if items/locations probably shouldn't be handled yet
            if game_state != 0x02 or link_control != 0x00 or link_priority != 0x11:
                return

            # Read all pending receive items and dump into game ram
            # if received_index <= len(ctx.items_received) - 1:
            for i in range(len(ctx.items_received) - received_index):
                write_result = False
                item = items_by_id[ctx.items_received[received_index + i].item]
                total = 0
                while not write_result:
                    # Write to the address if it hasn't changed
                    write_result = await bizhawk.guarded_write(
                        ctx.bizhawk_ctx,
                        [(0x3FA8, [item.byte_ids[0], item.byte_ids[1]], "IWRAM")],
                        [(0x3FA8, [0x0, 0x0], "IWRAM")]
                    )

                    await asyncio.sleep(0.05)
                    total += 0.05
                    if write_result:
                        total = 1
                    if total > 1:
                        break
                if not write_result:
                    break
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (0x3FE0E, [(received_index + i + 1) // 0x100, (received_index + i + 1) % 0x100], "EWRAM"),
                    ]
                )

            # Read all location flags in area and add to pending location checks if updates
            if room_area_id in self.location_by_room_area:
                for loc in self.location_by_room_area[room_area_id]:
                    if loc.id in self.local_checked_locations:
                        continue
                    loc_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(loc.ram_addr[0], 1, "EWRAM")])
                    if loc_bytes[0][0] | loc.ram_addr[1] == loc_bytes[0][0]:
                        # Add the the pending send list and the local checked locations to skip checking again
                        locs_to_send.add(loc.id)
                        self.local_checked_locations.add(loc.id)

            # Send location checks
            if len(locs_to_send) > 0:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

            # Player moved to a new room that isn't the pause menu. Pause menu `room_area_id` == 0x0000
            if self.room != room_area_id and room_area_id != 0x0000:
                # Location Scouting
                if self.room in self.location_by_room_area:
                    location_scouts = set()
                    for loc in self.location_by_room_area[self.room]:
                        if loc.id in self.local_checked_locations or loc.locType != LOC_TYPE_GROUND:
                            continue

                        location_scouts.add(loc.id)

                    if len(location_scouts) > 0:
                        await ctx.send_msgs(
                            [{
                                "cmd": "LocationScouts",
                                "locations": list(location_scouts),
                                "create_as_hint": 2
                            }]
                        )

                self.room = room_area_id
                # Room sync for poptracker tab tracking
                await ctx.send_msgs(
                    [{
                        "cmd": "Set",
                        "key": f"tmc_room_{ctx.team}_{ctx.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": room_area_id}]
                    }]
                )

            # Send game clear

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass
