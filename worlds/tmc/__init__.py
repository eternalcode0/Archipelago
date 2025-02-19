"""
Initialization module for The Legend of Zelda - The Minish Cap.
Handles the Web page for yaml generation, saving rom file and high-level generation.
"""

import pkgutil
import typing
from typing import Set
import os
import settings
from BaseClasses import Tutorial, Item, Region, Location, LocationProgressType, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Options import MinishCapOptions
from .Items import ItemData, itemList, item_frequencies, item_table, MinishCapItem
from .Locations import all_locations, location_table
from .Client import MinishCapClient
from .Regions import create_regions, connect_regions
from .Rom import MinishCapProcedurePatch, write_tokens
from .Rules import set_rules


class MinishCapWebWorld(WebWorld):
    """ Minish Cap Webpage configuration """

    theme = "grassFlowers"
    bug_report_page = "https://github.com/eternalcode0/Archipelago/issues"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to setting up The Legend of Zelda: The Minish Cap for Archipelago.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["eternalcode"],
        )
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
    item_name_to_id = {name: data.itemID for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    disabled_locations: Set[str]

    def generate_early(self) -> None:
        self.disabled_locations = set()

    # def create_location(self, region_name: str, location_name: str, local: bool):
    #     region = self.multiworld.get_region(region_name, self.player)
    #     location_id = self.location_name_to_id[location_name]
    #     location = Location(self.player, location_name, location_id, region)
    #     region.locations.append(location)
    #     if local:
    #         location.item_rule = lambda item: item.player == self.player

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)

        item = MinishCapItem("Victory", ItemClassification.progression, None, self.player)
        self.get_location("DWS - Green ChuChu").place_locked_item(item)

    def create_item(self, name: str) -> Item:
        item = item_table[name]
        return Item(name, item.classification, self.item_name_to_id[name], self.player)

    def create_items(self):
        # First add in all progression and useful items
        required_items = []
        precollected = [item for item in itemList if item in self.multiworld.precollected_items]
        for item in itemList:
            if item.classification not in (ItemClassification.filler, ItemClassification.skip_balancing):
                freq = item_frequencies.get(item.itemName, 1)
                if item in precollected:
                    freq = max(freq - precollected.count(item), 0)
                required_items += [item.itemName for _ in range(freq)]

        for item_name in required_items:
            self.multiworld.itempool.append(self.create_item(item_name))

        # Then compile a list of filler items based off their frequencies
        filler_items = []
        for item in itemList:
            if item.classification != ItemClassification.filler:
                continue
            freq = item_frequencies.get(item.itemName, 1)
            filler_items += [item.itemName for _ in range(freq)]

        # And finally take as many fillers as we need to have the same amount of items and locations.
        remaining = len(all_locations) - len(required_items) - len(self.disabled_locations)
        if remaining > 0:
            self.multiworld.itempool += [
                self.create_item(filler_item_name) for filler_item_name in self.random.sample(filler_items, remaining)
            ]

    def set_rules(self) -> None:
        set_rules(self, self.disabled_locations)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def generate_output(self, output_directory: str) -> None:
        patch = MinishCapProcedurePatch(player = self.player, player_name = self.multiworld.player_name[self.player])
        # patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff"))
        write_tokens(self, patch)
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}" f"{patch.patch_file_ending}"))
