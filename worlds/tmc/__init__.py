"""
Initialization module for The Legend of Zelda - The Minish Cap.
Handles the Web page for yaml generation, saving rom file and high-level generation.
"""

import logging
import os
import pkgutil
import typing
import settings
from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from Options import OptionError
from .Client import MinishCapClient
from .constants import MinishCapItem, MinishCapLocation, TMCEvent, TMCItem, TMCLocation
from .dungeons import fill_dungeons
from .Items import filler_item_selection, get_item_pool, get_pre_fill_pool, item_frequencies, item_groups, item_table, ItemData
from .Locations import all_locations, DEFAULT_SET, GOAL_PED, GOAL_VAATI, location_groups, OBSCURE_SET, POOL_RUPEE
from .Options import DungeonItem, get_option_data, MinishCapOptions, ShuffleElements
from .Regions import create_regions
from .Rom import MinishCapProcedurePatch, write_tokens
from .Rules import MinishCapRules

tmc_logger = logging.getLogger("The Minish Cap")


class MinishCapWebWorld(WebWorld):
    """ Minish Cap Webpage configuration """

    theme = "grassFlowers"
    bug_report_page = "https://github.com/eternalcode0/Archipelago/issues"
    tutorials = [
        Tutorial(tutorial_name="Setup Guide",
                 description="A guide to setting up The Legend of Zelda: The Minish Cap for Archipelago.",
                 language="English",
                 file_name="setup_en.md",
                 link="setup/en",
                 authors=["eternalcode"]),
        Tutorial(tutorial_name="Setup Guide",
                 description="A guide to setting up The Legend of Zelda: The Minish Cap for Archipelago.",
                 language="Français",
                 file_name="setup_fr.md",
                 link="setup/fr",
                 authors=["Deoxis9001"])
    ]


class MinishCapSettings(settings.Group):
    """ Settings for the launcher """

    class RomFile(settings.UserFilePath):
        """File name of the Minish Cap EU rom"""

        copy_to = "Legend of Zelda, The - The Minish Cap (Europe).gba"
        description = "Minish Cap ROM File"
        md5s = ["2af78edbe244b5de44471368ae2b6f0b"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class MinishCapWorld(World):
    """ Randomizer methods/data for generation """

    game = "The Minish Cap"
    web = MinishCapWebWorld()
    options_dataclass = MinishCapOptions
    options: MinishCapOptions
    settings: typing.ClassVar[MinishCapSettings]
    item_name_to_id = {name: data.item_id for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    item_name_groups = item_groups
    item_pool = []
    pre_fill_pool = []
    location_name_groups = location_groups
    disabled_locations: set[str]
    disabled_dungeons: set[str]

    def generate_early(self) -> None:
        tmc_logger.warning(
            "INCOMPLETE WORLD! Slot '%s' is using an unfinished alpha world that doesn't have all logic yet!",
            self.player_name)
        tmc_logger.warning("INCOMPLETE WORLD! Slot '%s' will require send_location/send_item for completion!",
                           self.player_name)

        enabled_pools = set(DEFAULT_SET)
        if self.options.rupeesanity.value:
            enabled_pools.add(POOL_RUPEE)
        if self.options.obscure_spots.value:
            enabled_pools |= OBSCURE_SET

        if self.options.shuffle_elements.value == ShuffleElements.option_dungeon_prize:
            self.options.start_hints.value.add(TMCItem.EARTH_ELEMENT)
            self.options.start_hints.value.add(TMCItem.FIRE_ELEMENT)
            self.options.start_hints.value.add(TMCItem.WATER_ELEMENT)
            self.options.start_hints.value.add(TMCItem.WIND_ELEMENT)

        self.disabled_locations = set(loc.name for loc in all_locations if not loc.pools.issubset(enabled_pools))

        # Check if the settings require more dungeons than are included
        self.disabled_dungeons = set(dungeon for dungeon in ["DWS", "CoF", "FoW", "ToD", "RC", "PoW"]
                                     if location_groups[dungeon].issubset(self.options.exclude_locations.value))

        if self.options.ped_dungeons > 6 - len(self.disabled_dungeons):
            error_message = "Slot '%s' has required %d/6 dungeons to goal but found %d excluded. "
            raise OptionError(error_message % (
                self.player_name,
                self.options.ped_dungeons,
                len(self.disabled_dungeons)))

    def fill_slot_data(self) -> dict[str, any]:
        data = {"DeathLink": self.options.death_link.value, "DeathLinkGameover": self.options.death_link_gameover.value,
                "RupeeSpot": self.options.rupeesanity.value, "ObscureSpot": self.options.obscure_spots.value,
                "GoalVaati": self.options.goal_vaati.value}
        data |= self.options.as_dict("death_link", "death_link_gameover", "rupeesanity", "obscure_spots",
                                     "goal_vaati", "random_bottle_contents", "weapon_bomb", "weapon_bow",
                                     "weapon_gust", "weapon_lantern",
                                     "tricks", "dungeon_small_keys", "dungeon_big_keys", "dungeon_compasses",
                                     "dungeon_maps",
                                     casing="snake")
        data |= get_option_data(self.options)
        # If Element location should be known, add locations to slot data for tracker
        if self.options.shuffle_elements.value in {ShuffleElements.option_dungeon_prize,
                                                   ShuffleElements.option_vanilla}:
            prizes = {TMCLocation.COF_PRIZE: "prize_cof", TMCLocation.CRYPT_PRIZE: "prize_rc",
                      TMCLocation.PALACE_PRIZE: "prize_pow", TMCLocation.DEEPWOOD_PRIZE: "prize_dws",
                      TMCLocation.DROPLETS_PRIZE: "prize_tod", TMCLocation.FORTRESS_PRIZE: "prize_fow"}
            for loc_name, data_name in prizes.items():
                placed_item = self.get_location(loc_name).item.name
                if placed_item in self.item_name_groups["Elements"]:
                    data[data_name] = item_table[placed_item].byte_ids[0]
        return data

    def create_regions(self) -> None:
        create_regions(self, self.disabled_locations, self.disabled_dungeons)

        loc = GOAL_VAATI if self.options.goal_vaati.value else GOAL_PED
        goal_region = self.get_region(loc.region)
        goal_item = MinishCapItem("Victory", ItemClassification.progression, None, self.player)
        goal_location = MinishCapLocation(self.player, loc.name, None, goal_region)
        goal_location.place_locked_item(goal_item)
        goal_region.locations.append(goal_location)
        # self.get_location(TMCEvent.CLEAR_PED).place_locked_item(self.create_event(TMCEvent.CLEAR_PED))

    def create_item(self, name: str) -> Item:
        item = item_table[name]
        return MinishCapItem(name, item.classification, self.item_name_to_id[name], self.player)

    def create_event(self, name: str) -> MinishCapItem:
        return MinishCapItem(name, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_item_selection)

    def create_items(self):
        # First add in all progression and useful items
        self.item_pool = get_item_pool(self)
        self.pre_fill_pool = get_pre_fill_pool(self)
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        for item in self.item_pool:
            self.multiworld.itempool.append(item)

        for _ in range(total_locations - len(self.item_pool) - len(self.pre_fill_pool)):
            self.multiworld.itempool.append(self.create_filler())

    def set_rules(self) -> None:
        MinishCapRules(self).set_rules(self.disabled_locations, self.location_name_to_id)
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "tmc_world.puml")

    def get_pre_fill_items(self) -> list[Item]:
        return self.pre_fill_pool

    def pre_fill(self) -> None:
        fill_dungeons(self)

    def generate_output(self, output_directory: str) -> None:
        patch = MinishCapProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff"))
        write_tokens(self, patch)
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}" f"{patch.patch_file_ending}"))
