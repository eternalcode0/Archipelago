import typing

from BaseClasses import Location


BASE_LOCATION_ID = 27022001000

class LocationData(typing.NamedTuple):
    id: int
    locCode: int
    name: str
    locBitMask: int

class MinishCapLocation(Location):
    game: str = "The Legend of Zelda - The Minish Cap"

smith_house: typing.List[LocationData] = [
    LocationData(27022001000, 0x2CDE, "Smith House Chest", 0x40),
]

intro_town: typing.List[LocationData] = [
    LocationData(27022001002, 0x2B35, "Town Intro - Small Shield", 0x04),
]

intro_castle: typing.List[LocationData] = [
    LocationData(27022001001, 0x2B32, "Castle Intro - Smith's Sword", 0x04),
]

minish_village: typing.List[LocationData] = [
    LocationData(27022001003, 0x2B48, "Minish Village - Barrel", 0x40),
]

dungeon_dws: typing.List[LocationData] = [
    LocationData(27022001004, 0x2B3F, "DWS - Gust Jar", 0x08),
    LocationData(27022001005, 0x2D45, "DWS - Heart Piece after Madderpillar", 0x80),
    LocationData(27022001006, 0x2D45, "DWS - Red Rupee Chest before Boss", 0x04),
    LocationData(27022001007, 0x2D44, "DWS - Boss Heart Container", 0x80),
]

goal: typing.List[LocationData] = [
    LocationData(None, None, "DWS - Green ChuChu", None)
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
