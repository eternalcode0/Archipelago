import typing

if typing.TYPE_CHECKING:
    from . import MinishCapWorld


class TMCRegion:
    SOUTH_FIELD = "South Field"
    NORTH_FIELD = "North Field"
    CASTLE_EXTERIOR = "Castle Exterior"
    EASTERN_HILLS = "Eastern Hills"
    LONLON = "LonLon"
    LOWER_FALLS = "Lower Falls"
    LAKE_HYLIA_NORTH = "Lake Hylia North"
    LAKE_HYLIA_SOUTH = "Lake Hylia South"
    MINISH_WOODS = "Minish Woods"
    TRILBY_HIGHLANDS = "Trilby Highlands"
    WESTERN_WOODS = "Western Woods"
    CRENEL_BASE = "Crenel Base"
    CRENEL = "Crenel"
    MELARI = "Melari"
    CASTOR_WILDS = "Castor Wilds"
    WIND_RUINS = "Ruins"
    ROYAL_VALLEY = "Royal Valley"
    GRAVEYARD = "Graveyard"
    DUNGEON_RC = "Dungeon RC"
    UPPER_FALLS = "Upper Falls"
    CLOUDS = "Clouds"
    WIND_TRIBE = "Wind Tribe"
    DUNGEON_DWS = "Deepwood Shrine"
    DUNGEON_COF = "Cave of Flames"
    DUNGEON_FOW = "Fortress of Winds"
    DUNGEON_TOD = "Temple of Droplets"
    DUNGEON_TOD_MAIN = "Temple of Droplets After Big key"
    DUNGEON_POW = "Palace of Winds"
    SANCTUARY = "Sanctuary"
    DUNGEON_DHC = "Dark Hyrule Castle"
    HYRULE_TOWN = "Hyrule Town"

all_regions = [
    TMCRegion.SOUTH_FIELD,
    TMCRegion.NORTH_FIELD,
    TMCRegion.CASTLE_EXTERIOR,
    TMCRegion.EASTERN_HILLS,
    TMCRegion.LONLON,
    TMCRegion.LOWER_FALLS,
    TMCRegion.LAKE_HYLIA_NORTH,
    TMCRegion.LAKE_HYLIA_SOUTH,
    TMCRegion.MINISH_WOODS,
    TMCRegion.TRILBY_HIGHLANDS,
    TMCRegion.WESTERN_WOODS,
    TMCRegion.CRENEL_BASE,
    TMCRegion.CRENEL,
    TMCRegion.MELARI,
    TMCRegion.CASTOR_WILDS,
    TMCRegion.WIND_RUINS,
    TMCRegion.ROYAL_VALLEY,
    TMCRegion.GRAVEYARD,
    TMCRegion.DUNGEON_RC,
    TMCRegion.UPPER_FALLS,
    TMCRegion.CLOUDS,
    TMCRegion.WIND_TRIBE,
    TMCRegion.DUNGEON_DWS,
    TMCRegion.DUNGEON_COF,
    TMCRegion.DUNGEON_FOW,
    TMCRegion.DUNGEON_TOD,
    TMCRegion.DUNGEON_TOD_MAIN,
    TMCRegion.DUNGEON_POW,
    TMCRegion.SANCTUARY,
    TMCRegion.DUNGEON_DHC,
    TMCRegion.HYRULE_TOWN,
]
