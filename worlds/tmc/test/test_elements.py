from worlds.tmc.constants import TMCItem, TMCLocation
from worlds.tmc.options import ShuffleElements
from worlds.tmc.test import MinishCapTestBase


class TestElementsVanilla(MinishCapTestBase):
    options = {
        "shuffle_elements": ShuffleElements.option_vanilla,
    }

    def test_elements_vanilla(self) -> None:
        """Test that each of the elements gets placed in its vanilla location"""
        prize_names = [
            TMCLocation.DEEPWOOD_PRIZE,
            TMCLocation.COF_PRIZE,
            TMCLocation.DROPLETS_PRIZE,
            TMCLocation.PALACE_PRIZE,
        ]
        prizes = [TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT]
        locations = [self.multiworld.get_location(prize_name, self.player) for prize_name in prize_names]
        for (location, prize) in zip(locations, prizes):
            self.assertEqual(location.item.name, prize)


class TestElementsVanillaExcluded(MinishCapTestBase):
    options = {
        "shuffle_elements": ShuffleElements.option_vanilla,
        "exclude_locations": ["Palace Prize", "Crypt Prize"],
    }

    def test_elements_vanilla_excluded(self) -> None:
        """Test that each of the elements gets placed in its vanilla location while ignoring exclude_locations"""
        prize_names = [
            TMCLocation.DEEPWOOD_PRIZE,
            TMCLocation.COF_PRIZE,
            TMCLocation.DROPLETS_PRIZE,
            TMCLocation.PALACE_PRIZE,
        ]
        prizes = [TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT]
        locations = [self.multiworld.get_location(prize_name, self.player) for prize_name in prize_names]
        for (location, prize) in zip(locations, prizes):
            self.assertEqual(location.item.name, prize)


class TestElementsPrizes(MinishCapTestBase):
    options = {
        "shuffle_elements": ShuffleElements.option_dungeon_prize,
    }

    def test_elements_prizes(self) -> None:
        """Test that each of the elements is placed into a prize location"""
        locations = {
            TMCLocation.DEEPWOOD_PRIZE,
            TMCLocation.COF_PRIZE,
            TMCLocation.FORTRESS_PRIZE,
            TMCLocation.DROPLETS_PRIZE,
            TMCLocation.CRYPT_PRIZE,
            TMCLocation.PALACE_PRIZE,
        }
        prizes = {TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT}
        for prize in prizes:
            placements = self.multiworld.find_item_locations(prize, self.player)
            self.assertEqual(len(placements), 1, "Multiple of the same element was placed")
            self.assertIn(placements[0].name, locations, "Element was placed outside a prize location")


class TestElementsPrizesExcluded(MinishCapTestBase):
    options = {
        "shuffle_elements": ShuffleElements.option_dungeon_prize,
        "exclude_locations": ["Palace Prize", "Crypt Prize"],
    }

    def test_elements_prizes_excluded(self) -> None:
        """Test that each of the elements is placed into a prize location"""
        locations = {
            TMCLocation.DEEPWOOD_PRIZE,
            TMCLocation.COF_PRIZE,
            TMCLocation.FORTRESS_PRIZE,
            TMCLocation.DROPLETS_PRIZE,
        }
        prizes = {TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT}
        for prize in prizes:
            placements = self.multiworld.find_item_locations(prize, self.player)
            self.assertEqual(len(placements), 1, "Multiple of the same element was placed")
            self.assertIn(placements[0].name, locations, "Element was placed outside a prize location")


class TestElementsAnywhere(MinishCapTestBase):
    """Stub test to ensure generation succeeds when ElementShuffle == anywhere"""
    options = {
        "shuffle_elements": ShuffleElements.option_anywhere,
    }
