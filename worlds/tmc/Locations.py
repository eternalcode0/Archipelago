import typing

from BaseClasses import Location


BASE_LOCATION_ID = 27022001000

class LocationData(typing.NamedTuple):
    id: int
    name: str
    """The address in the rom for placing items"""
    romLoc: int
    """1st = The address in EWRAM to read/write to, 2nd = The bit mask for the address"""
    locCode: typing.Tuple[int,int]
    """The area (1st byte) and room (2nd byte) the check is found in"""
    roomArea: int

class MinishCapLocation(Location):
    game: str = "The Legend of Zelda - The Minish Cap"


smith_house: typing.List[LocationData] = [
    LocationData(27022001000, "Smith House Chest", 0xf25aa, (0x2CDE, 0x40), 0x1122),
]

intro_town: typing.List[LocationData] = [
    LocationData(27022001002, "Town Intro - Small Shield", None, (0x2C9F, 0x10), 0x0015),
]

intro_castle: typing.List[LocationData] = [
    LocationData(27022001001, "Castle Intro - Smith's Sword", None, (0x2B3F, 0x04), 0x0280), # Technically belongs to the given broken picori blade but you get both at the same time anyway
]

minish_village: typing.List[LocationData] = [
    LocationData(27022001003, "Minish Village - Barrel", None, (0x2B48, 0x40), 0x0920),
]

dungeon_dws: typing.List[LocationData] = [
    LocationData(27022001004, "DWS - Gust Jar", None, (0x2D3F, 0x08), 0x0048),
    LocationData(27022001005, "DWS - Heart Piece after Madderpillar", None, (0x2D46, 0x04), 0x0548),
    LocationData(27022001006, "DWS - Red Rupee Chest before Boss", None, (0x2D45, 0x04), 0x1748),
    LocationData(27022001007, "DWS - Boss Heart Container", None, (0x2D44, 0x80), 0x0049),
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

# target: typing.Dict[int, [LocationData]] = {
#     0x0048: [LocationData()],
#     0x0548: [LocationData(), LocationData()],
# }

goal: typing.List[LocationData] = [
    LocationData(None, "DWS - Green ChuChu", None, None, None)
]

preSeedLocations: typing.List[MinishCapLocation] = [
    MinishCapLocation(0x0f2f86, "thing", 0x00),
]

all_locations: typing.List[MinishCapLocation] = (smith_house
    + intro_town
    + intro_castle
    + minish_village
    + dungeon_dws
)



location_table: typing.Dict[str, int] = {location.name: location.locCode for location in all_locations}
