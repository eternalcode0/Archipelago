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
    LAKE_HYLIA = "Lake Hylia"
    MINISH_WOODS = "Minish Woods"
    TRILBY_HIGHLANDS = "Trilby Highlands"
    WESTERN_WOODS = "Western Woods"
    CRENEL = "Crenel"
    CASTOR_WILDS = "Castor Wilds"
    RUINS = "Ruins"
    VALLEY = "Valley"
    DUNGEON_RC = "Dungeon RC"
    UPPER_FALLS = "Upper Falls"
    CLOUDS = "Clouds"
    WIND_TRIBE = "Wind Tribe"
    DUNGEON_DWS = "Deepwood Shrine"
    DUNGEON_COF = "Cave of Flames"
    DUNGEON_FOW = "Fortress of Winds"
    DUNGEON_TOD = "Temple of Droplets"
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
    TMCRegion.LAKE_HYLIA,
    TMCRegion.MINISH_WOODS,
    TMCRegion.TRILBY_HIGHLANDS,
    TMCRegion.WESTERN_WOODS,
    TMCRegion.CRENEL,
    TMCRegion.CASTOR_WILDS,
    TMCRegion.RUINS,
    TMCRegion.VALLEY,
    TMCRegion.DUNGEON_RC,
    TMCRegion.UPPER_FALLS,
    TMCRegion.CLOUDS,
    TMCRegion.WIND_TRIBE,
    TMCRegion.DUNGEON_DWS,
    TMCRegion.DUNGEON_COF,
    TMCRegion.DUNGEON_FOW,
    TMCRegion.DUNGEON_TOD,
    TMCRegion.DUNGEON_POW,
    TMCRegion.SANCTUARY,
    TMCRegion.DUNGEON_DHC,
    TMCRegion.HYRULE_TOWN,
]
