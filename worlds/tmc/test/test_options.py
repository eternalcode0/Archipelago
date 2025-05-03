from . import MinishCapTestBase
from ..constants import TMCLocation, TMCItem
from ..Options import ShuffleElements, DungeonItem


class TestElementsVanilla(MinishCapTestBase):
    options = {
        "shuffle_elements": ShuffleElements.option_vanilla,
    }

    def test_elements_vanilla(self) -> None:
        """Test that each of the elements gets placed in it's vanilla location"""
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
        "shuffle_elements": ShuffleElements.option_dungeon_prize
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

class TestElementsAnywhere(MinishCapTestBase):
    """Stub test to ensure generation succeeds when ElementShuffle == anywhere"""
    options = {
        "shuffle_elements": ShuffleElements.option_anywhere
    }

class TestSmallKeysDungeon(MinishCapTestBase):
    options = {
        "dungeon_small_keys": DungeonItem.option_own_dungeon
    }

class TestBigKeysDungeon(MinishCapTestBase):
    options = {
        "dungeon_big_keys": DungeonItem.option_own_dungeon
    }
