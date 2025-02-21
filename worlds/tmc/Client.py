from typing import TYPE_CHECKING, Set, Dict

import asyncio


import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Locations import all_locations, LocationData
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
    "received_index": (0x2A4A, 2, "EWRAM"),
}

class MinishCapClient(BizHawkClient):
    game = "The Minish Cap"
    system = "GBA"
    patch_suffix = ".aptmc"
    local_checked_locations: Set[int]
    location_name_to_id: Dict[str, int]
    location_by_room_area: Dict[int, [LocationData]]

    def __init__(self) -> None:
        super().__init__()
        self.location_name_to_id = {loc_data.name: loc_data.locCode for loc_data in all_locations}
        self.local_checked_locations = set()
        self.location_by_room_area = {}

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
            print(rom_name)
            if rom_name != "GBAZELDA":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True
        ctx.watcher_timeout = 1

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
            ])
            if read_result is None:
                return
            # [game_state, room_area_id] = read_result
            game_state = read_result[0][0]
            room_area_id = int.from_bytes(read_result[1], "little")
            link_control = read_result[2][0]
            link_priority = read_result[3][0]
            received_index = (read_result[4][0] << 8) + read_result[4][1]

            locs_to_send = set()

            # Early return if items/locations probably shouldn't be handled yet
            if game_state != 0x02 or link_control != 0x00 or link_priority != 0x11:
                return

            # Read all pending receive items and dump into game ram
            if received_index <= len(ctx.items_received) - 1:
                for i, item in enumerate(ctx.items_received, received_index):
                    write_result = False
                    item = items_by_id[ctx.items_received[i].item]
                    if item.address is None:
                        continue
                    ram_address, bit_flag = item.address
                    total = 0
                    while not write_result:
                        read_result: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(ram_address, 1, "EWRAM")]))[0]
                        current = int.from_bytes(read_result, "little")
                        new: int = current | bit_flag

                        # Write to the address if it hasn't changed
                        write_result: bool = await bizhawk.guarded_write(
                            ctx.bizhawk_ctx,
                            [(ram_address, [new], "EWRAM")],
                            [(ram_address, [current], "EWRAM")]
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
                            (0x2A4A, [(received_index + i + 1) // 0x100, (received_index + i + 1) % 0x100], "EWRAM"),
                        ]
                    )

            # Read all location flags in area and add to pending location checks if updates
            if room_area_id in self.location_by_room_area:
                for loc in self.location_by_room_area[room_area_id]:
                    if loc.id in self.local_checked_locations:
                        continue
                    loc_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(loc.locCode[0], 1, "EWRAM")])
                    if loc_bytes[0][0] | loc.locCode[1] == loc_bytes[0][0]:
                        # Add the the pending send list and the local checked locations to skip checking again
                        locs_to_send.add(loc.id)
                        self.local_checked_locations.add(loc.id)

            # Send location checks
            if locs_to_send is not None:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

            # Send game clear

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass
