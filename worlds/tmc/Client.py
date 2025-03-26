from typing import TYPE_CHECKING, Set, Dict

import asyncio

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Locations import all_locations, LocationData, events
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
    "game_task": (0x1002, 1, "IWRAM"),
    # 0x00 = Initialise Room
    # 0x01 = Change Room
    # 0x02 = Update
    # 0x03 = Change Area
    # 0x04 = Minish Portal
    # 0x05 = Barrel Update
    # 0x06 = Reserved
    # 0x07 = Subtask
    "task_substate": (0x1004, 1, "IWRAM"),
    # The room id in the 1st byte, area id in the 2nd
    "room_area_id": (0x0BF4, 2, "IWRAM"),
    # 0x00 Denotes whether the player can input, 0x01 cannot input. Not to be confused with can move/interact.
    # Can still be set to 0x00 when the player is in confusing situations such as reading textboxes
    "action_state": (0x116C, 1, "IWRAM"),
    # 0x11: Standard gameplay
    # 0x12: Reading dialog?
    # 0x13: Growing (yes, there's a separate state for growing from minish and none for shrinking)
    # 0x16: Watching Cutscene
    "link_priority": (0x1171, 1, "IWRAM"),
    # An arbitrary address that isn't used strictly by the game
    # We'll use it to store the index of the last processed remote item
    "received_index": (0x3FF00, 2, "EWRAM"),
    "vaati_address": (0x2CA6, 1, "EWRAM"),
    "link_health": (0x11A5, 1, "IWRAM"),
    "gameover": (0x10A5, 1, "IWRAM"),
}


class MinishCapClient(BizHawkClient):
    game = "The Minish Cap"
    system = "GBA"
    patch_suffix = ".aptmc"
    local_checked_locations: Set[int]
    location_name_to_id: Dict[str, int]
    location_by_room_area: Dict[int, [LocationData]]
    room: int
    previous_death_link = 0
    death_link_ready = False
    ignore_next_death_link = False
    event_data = list(map(lambda e: (e[0], 1, "EWRAM"), events.keys()))
    events_sent = set()

    def __init__(self) -> None:
        super().__init__()
        self.location_name_to_id = {loc_data.name: loc_data.ram_addr for loc_data in all_locations}
        self.local_checked_locations = set()
        self.location_by_room_area = {}
        self.room = 0x0000

        for loc in all_locations:
            if loc.room_area in self.location_by_room_area:
                self.location_by_room_area[loc.room_area].append(loc)
            else:
                self.location_by_room_area[loc.room_area] = [loc]

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
        ctx.watcher_timeout = 0.5

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        try:
            # Handle giving the player items
            read_result = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_task"], # Current state of game (is the player actually in-game?)
                RAM_ADDRS["task_substate"], # Is there any room transitions or anything similar
                RAM_ADDRS["room_area_id"],
                RAM_ADDRS["action_state"],
                RAM_ADDRS["link_priority"],
                RAM_ADDRS["received_index"],
                RAM_ADDRS["vaati_address"],
                RAM_ADDRS["link_health"],
                RAM_ADDRS["gameover"],
            ])
            if read_result is None:
                return

            game_task = read_result[0][0]
            task_substate = read_result[1][0]
            room_area_id = int.from_bytes(read_result[2], "little")
            action_state = read_result[3][0]
            link_priority = read_result[4][0]
            received_index = (read_result[5][0] << 8) + read_result[5][1]
            vaati_address = read_result[6][0]
            link_health = int.from_bytes(read_result[7], "little")
            gameover = bool.from_bytes(read_result[8])

            # Check for goal, since vaati's defeat triggers a cutscene this has to be checked before the next if
            # specifically because it sets the game_task to 0x04
            if not ctx.finished_game and vaati_address | 0x02 == vaati_address:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

            # Only process items/locations if the player is in "normal" gameplay
            if game_task == 0x02 or task_substate == 0x02:
                await self.handle_item_receiving(ctx, received_index)
                await self.handle_location_sending(ctx, room_area_id)
                await self.handle_event_setting(ctx)

            # Death link handling only if in normal gameplay (0x02) or gamemover (0x03)
            if game_task in range(0x02, 0x04) and ctx.slot_data.get("DeathLink", 0) == 1:
                await self.handle_death_link(ctx, link_health, gameover, action_state)

            # Player moved to a new room that isn't the pause menu. Pause menu `room_area_id` == 0x0000
            if task_substate == 0x02 and self.room != room_area_id:
                await self.handle_room_change(ctx, room_area_id)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def handle_item_receiving(self, ctx: "BizHawkClientContext", received_index: int) -> None:
        # Read all pending receive items and dump into game ram
        for i in range(len(ctx.items_received) - received_index):
            write_result = False
            item = items_by_id[ctx.items_received[received_index + i].item]
            total = 0
            while not write_result:
                # Write to the address if it hasn't changed
                write_result = await bizhawk.guarded_write(
                    ctx.bizhawk_ctx,
                    [(0x3FF10, [item.byte_ids[0], item.byte_ids[1]], "EWRAM")],
                    [(0x3FF10, [0x0, 0x0], "EWRAM")]
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
                    (0x3FF00, [(received_index + i + 1) // 0x100, (received_index + i + 1) % 0x100], "EWRAM"),
                ]
            )

    async def handle_location_sending(self, ctx: "BizHawkClientContext", room_area_id: int) -> None:
        locs_to_send = set()
        # Read all location flags in area and add to pending location checks if updates
        if room_area_id in self.location_by_room_area:
            for loc in self.location_by_room_area[room_area_id]:
                if loc.id in self.local_checked_locations or loc.id not in ctx.server_locations:
                    continue
                loc_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(loc.ram_addr[0], 1, "EWRAM")])
                if loc_bytes[0][0] | loc.ram_addr[1] == loc_bytes[0][0]:
                    # Add the the pending send list and the local checked locations to skip checking again
                    locs_to_send.add(loc.id)
                    self.local_checked_locations.add(loc.id)
        # Send location checks
        if len(locs_to_send) > 0:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

    async def handle_death_link(self, ctx: "BizHawkClientContext", link_health: int, game_over: bool, action_state: int) -> None:
        if "DeathLink" not in ctx.tags:
            await ctx.update_death_link(True)
            self.previous_death_link = ctx.last_death_link

        # If we processed a death on a previous loop
        if not self.death_link_ready:
            # Wait until player is not in a game_over state
            if link_health > 0 and not game_over:
                self.death_link_ready = True
            # And/or return out of processing
            return

        gameover_mode = ctx.slot_data.get("DeathLinkGameover", 0) == 1
        # If a new death link has come in different from the last
        if self.previous_death_link != ctx.last_death_link and (link_health > 0 or not game_over):
            self.previous_death_link = ctx.last_death_link # record the newest death link
            if self.ignore_next_death_link:
                self.ignore_next_death_link = False
            else:
                if gameover_mode:
                    # Death should gameover, do not pass go, do not collect 200 rupees.
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(RAM_ADDRS["gameover"][0], [1], "IWRAM")]
                    )
                    self.death_link_ready = False
                elif not gameover_mode:
                    # Death should not gameover, give an opportunity for fairy revive.
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(RAM_ADDRS["link_health"][0], [0], "IWRAM")]
                    )
                    self.death_link_ready = False
        # Not receiving death, decide if we send death
        if gameover_mode and action_state == 0x0A:
            if game_over:
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} ran out of fairies!")
                self.death_link_ready = False
                self.ignore_next_death_link = True
        elif action_state == 0x0A:
            if link_health == 0:
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} ran out of hearts!")
                self.death_link_ready = False
                self.ignore_next_death_link = True

    async def handle_room_change(self, ctx: "BizHawkClientContext", room_area_id) -> None:
        # Location Scouting
        if self.room in self.location_by_room_area:
            location_scouts = set()
            for loc in self.location_by_room_area[self.room]:
                if loc.id in self.local_checked_locations or not loc.scoutable:
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

    async def handle_event_setting(self, ctx: "BizHawkClientContext") -> None:
        # Batch all events together into one read
        read_events = await bizhawk.read(ctx.bizhawk_ctx, self.event_data)

        if read_events is None:
            return

        for i, (address_pair, event_name) in enumerate(events.items()):
            if event_name in self.events_sent or read_events[i][0] | address_pair[1] != read_events[i][0]:
                continue
            self.events_sent.add(event_name)
            await ctx.send_msgs(
                [{
                    "cmd": "Set",
                    "key": f"tmc_{event_name}_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "replace", "value": 1}]
                }]
            )
