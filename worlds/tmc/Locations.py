import typing

from BaseClasses import Location
from .Constants import LocationName


BASE_LOCATION_ID = 27022001000

LOC_TYPE_CHEST = 0
LOC_TYPE_GROUND = 1

class LocationData(typing.NamedTuple):
    id: int
    name: str
    """The address in the rom for placing items"""
    romLoc: int
    """1st = The address in EWRAM to read/write to, 2nd = The bit mask for the address"""
    locCode: typing.Tuple[int,int]
    """
    The area (1st byte) and room (2nd byte) the check is found in. Intended to help filter the number of locations
    iterated per game watcher loop. Also helps keep track of whether items in the area need to be location scouted.
    """
    roomArea: int
    """0 = Chest, 1 = Ground Item. Intended to be used for location scouts."""
    locType: int

class MinishCapLocation(Location):
    game: str = "The Minish Cap"


smith_house: typing.List[LocationData] = [
    LocationData(27022001000, LocationName.SMITH_HOUSE_RUPEE, 0xF25AA, (0x2CDE, 0x40), 0x1122, LOC_TYPE_CHEST),
    LocationData(27022001001, LocationName.SMITH_HOUSE_SWORD, None, (0x2CF5, 0x01), 0x1122, LOC_TYPE_GROUND), # New location from base patch after intro skip
    LocationData(27022001002, LocationName.SMITH_HOUSE_SHIELD, None, (0x2CF5, 0x02), 0x1122, LOC_TYPE_GROUND), # New location from base patch after intro skip
]

hyrule_town: typing.List[LocationData] = []

minish_village: typing.List[LocationData] = [
    LocationData(27022001003, LocationName.MINISH_VILLAGE_BARREL_HOUSE, None, (0x2B48, 0x40), 0x0920, LOC_TYPE_GROUND),
]

dungeon_dws: typing.List[LocationData] = [
    LocationData(27022001004, LocationName.DWS_GUST_JAR, None, (0x2D3F, 0x08), 0x0048, LOC_TYPE_CHEST),
    LocationData(27022001005, LocationName.DWS_MADDERPILLAR_HEART_PIECE, None, (0x2D46, 0x04), 0x0548, LOC_TYPE_GROUND),
    LocationData(27022001006, LocationName.DWS_2F_RED_RUPEE, None, (0x2D45, 0x04), 0x1748, LOC_TYPE_CHEST),
    LocationData(27022001007, LocationName.DWS_BOSS_HEART_CONTAINER, None, (0x2D44, 0x80), 0x0049, LOC_TYPE_GROUND),
    # LocationData(27022001008, "DWS - Slug Torch Room - Small Key", None, None, 0x1048),
    # LocationData(27022001009, "DWS - Dungeon Map Chest", None, None, 0x0548),
    # LocationData(27022001010, "DWS - 2 Pillar Room - Small Key", None, None, 0x0448),
    # LocationData(27022001011, "DWS - Monster Room - Small Key", None, None, 0x0848),
    # LocationData(27022001012, "DWS - Dungeon Compass Chest", None, None, 0x1248),
    # LocationData(27022001013, "DWS - 10 Mysterious Shell Chest", None, None, 0x0648),
    # LocationData(27022001014, "DWS - B2F Small Key Chest", None, None, 0x1248),
    # LocationData(27022001015, "DWS - 20 Mysterious Shell Chest", None, None, 0x0248),
    # LocationData(27022001016, "DWS - Boss Key Chest", None, None, 0x1148),
    # LocationData(27022001017, "DWS - Blue Portal Heart Piece", None, None, 0x0148),
]

goal: typing.List[LocationData] = [
    LocationData(None, "DWS - Green ChuChu", None, None, None, None)
]

all_locations: typing.List[MinishCapLocation] = (smith_house
    + hyrule_town
    + minish_village
    + dungeon_dws
)

location_table_by_name: typing.Dict[str, int] = {location.name: location for location in all_locations}
