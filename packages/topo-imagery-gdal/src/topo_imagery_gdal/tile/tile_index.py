import re
from typing import NamedTuple

from topo_imagery_common.epsg import EpsgNumber
from topo_imagery_gdal.tile.util import charcodeat

SHEET_WIDTH = 24_000
""" Width of Topo 1:50k mapsheets (meters) """
SHEET_HEIGHT = 36_000
""" Height of Topo 1:50k mapsheets (meters) """
SHEET_ORIGIN_LEFT = 988_000
""" The NZTM x coordinate of the left edge of 1:50k mapsheets which would be at column position 00 """
SHEET_ORIGIN_TOP = 6_234_000
""" The NZTM y coordinate of the top edge of 1:50k mapsheets in row AS (the northernmost row) """
GRID_SIZE_MAX = 50_000
""" Base scale Topo 1:50k mapsheets (meters) """
CHAR_A = charcodeat("A", 0)
CHAR_S = charcodeat("S", 0)


class Point(NamedTuple):
    """Class that represents a point(x,y)"""

    x: int | float
    y: int | float


class Size(NamedTuple):
    width: int | float
    height: int | float


class Bounds(NamedTuple):
    point: Point
    size: Size


# The six Chatham Islands Topo50 mapsheets (EPSG:3793, NZGD2000 / Chatham Islands TM 2000), laid
# out on the same 24,000m x 36,000m 1:50k grid as the mainland sheets, with a different origin
# and layout of sheet codes. The following sheet codes are used:
# +------+------+------+
# | CI01 | CI02 | CI03 |
# |      |      |      |
# +------+------+------+
#        | CI04 | CI05 |
#        |      |      |
#        +------+------+
#               | CI06 |
#               |      |
#               +------+
# Reference:
# https://data.linz.govt.nz/layer/50089-nz-chatham-island-linz-map-sheets-topo-150k/
CHATHAM_SHEET_ORIGINS: dict[str, Point] = {
    "CI01": Point(x=3_458_000, y=5_176_000),  # Point Somes
    "CI02": Point(x=3_482_000, y=5_176_000),  # Cape Young
    "CI03": Point(x=3_506_000, y=5_176_000),  # Kaingaroa
    "CI04": Point(x=3_482_000, y=5_140_000),  # Waitangi
    "CI05": Point(x=3_506_000, y=5_140_000),  # Owenga
    "CI06": Point(x=3_506_000, y=5_104_000),  # Pitt Island (Rangiauria)
}

def get_bounds_from_name(tile_name: str, target_epsg: int = EpsgNumber.NZTM_2000) -> Bounds:
    """Get the origin coordinates and size of the tile from its name.

    Args:
        tile_name: the tile name as `sheetCode_gridSize_tileId`
        target_epsg: EPSG code of the mapsheet grid for the tile.
            `EpsgNumber.NZTM_2000` (2193) and `EpsgNumber.CITM_2000` (3793) are supported

    Returns:
        a `Bounds` object
    """
    if target_epsg == EpsgNumber.NZTM_2000:
        get_offset = get_mapsheet_offset
    elif target_epsg == EpsgNumber.CITM_2000:
        get_offset = get_chatham_mapsheet_offset
    else:
        raise ValueError(
            f"Unsupported target EPSG:{target_epsg} for mapsheet lookup. "
            f"Supported: {EpsgNumber.NZTM_2000.value}, {EpsgNumber.CITM_2000.value}"
        )

    # check for 50k imagery
    if re.match(r"^[A-Z]{2}\d{2}$", tile_name):
        origin = get_offset(tile_name)
        return Bounds(
            Point(x=origin.x, y=origin.y),
            Size(SHEET_WIDTH, SHEET_HEIGHT),
        )

    name_parts = tile_name.split("_")
    map_sheet = name_parts[0]
    # should be in [10_000, 5_000, 2_000, 1_000, 500]
    grid_size = int(name_parts[1])

    x = int(name_parts[2][-2:])
    y = int(name_parts[2][:2])
    if grid_size == 500:
        x = int(name_parts[2][-3:])
        y = int(name_parts[2][:3])

    origin = get_offset(map_sheet)
    tile_offset = get_tile_offset(grid_size=grid_size, x=x, y=y)
    return Bounds(
        Point(x=origin.x + tile_offset.point.x, y=origin.y - tile_offset.point.y),
        Size(tile_offset.size.width, tile_offset.size.height),
    )


def get_mapsheet_offset(sheet_code: str) -> Point:
    """Convert a mapsheet code into the origin point for the mapsheet

    Args:
        sheet_code: topo 50 map sheet code eg "CG10"

    Returns:
        Point: The top left point of the mapsheet

    Example:
        >>> get_mapsheet_offset("CG10")
        Point(x=1228000, y=4866000)
    """

    # from a mapsheet of "CG10", Y offset is "CG", X offset is 10
    # Y:"CG" x:"10"
    x = int(sheet_code[-2:])  # x = 10

    ms = sheet_code[:2]  # 'CG'
    # position difference of "S" and "A" as mapsheets start at "AS"
    base_y_offset = CHAR_S - CHAR_A
    # "C" -> C:67 - A:65 = 2 * 26 (Mapsheet codes A-Z)
    first_letter_offset = (charcodeat(ms, 0) - CHAR_A) * 26
    # "G" -> G:71 - A:65 = 6
    second_letter_offset = charcodeat(ms, 1) - CHAR_A

    y = first_letter_offset + second_letter_offset - base_y_offset

    # There are three missing map sheets
    if ms > "CI":
        y -= 3
    elif ms > "BO":
        y -= 2
    elif ms > "BI":
        y -= 1

    return Point(x=SHEET_WIDTH * x + SHEET_ORIGIN_LEFT, y=SHEET_ORIGIN_TOP - SHEET_HEIGHT * y)


def get_chatham_mapsheet_offset(sheet_code: str) -> Point:
    """Look up the origin point for a Chatham Islands mapsheet code.

    Args:
        sheet_code: Chatham Islands topo 50 map sheet code eg "CI06"

    Returns:
        Point: The top left point of the mapsheet, in EPSG:3793

    Example:
        >>> get_chatham_mapsheet_offset("CI06")
        Point(x=3506000, y=5104000)
    """
    origin = CHATHAM_SHEET_ORIGINS.get(sheet_code[:4])
    if origin is None:
        raise ValueError(f"Unknown Chatham Islands map sheet: {sheet_code}. Known sheets: {sorted(CHATHAM_SHEET_ORIGINS)}")
    return origin


def get_tile_offset(grid_size: int, x: int, y: int) -> Bounds:
    """Get the tile offset from its coordinate and the grid size

    Args:
        grid_size: a size in [10_000, 5_000, 2_000, 1_000, 500]
        x: upper left coordinate x
        y: upper left coordinate y

    Returns:
        a `Bounds` object
    """
    scale = grid_size / GRID_SIZE_MAX
    offset_x = SHEET_WIDTH * scale
    offset_y = SHEET_HEIGHT * scale
    return Bounds(Point(x=(x - 1) * offset_x, y=(y - 1) * offset_y), Size(width=offset_x, height=offset_y))
