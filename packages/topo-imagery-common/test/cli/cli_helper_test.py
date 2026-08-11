from argparse import ArgumentTypeError
from datetime import datetime
from decimal import Decimal
from typing import Any

from pytest import raises
from pytest_subtests import SubTests
from shapely.geometry import MultiPolygon
from topo_imagery_common.cli.cli_helper import (
    TileFiles,
    coalesce_multi_single,
    get_geometry_from_geojson_feature,
    get_non_empty_features,
    get_tile_files,
    parse_list,
    str_to_bool,
    str_to_gsd,
    str_to_list_or_none,
    str_to_positive_int,
    valid_date,
)


def test_get_tile_files(subtests: SubTests) -> None:
    file_source = '[{"output": "tile_name","input": ["file_a.tiff", "file_b.tiff"]}, \
    {"output": "tile_name2","input": ["file_a.tiff", "file_b.tiff"]}]'
    expected_output_filename = "tile_name"
    expected_output_filename_b = "tile_name2"
    expected_input_filenames = ["file_a.tiff", "file_b.tiff"]

    source: list[TileFiles] = get_tile_files(file_source)
    with subtests.test():
        assert expected_output_filename == source[0].output

    with subtests.test():
        assert expected_input_filenames == source[0].inputs

    with subtests.test(msg="Should not include derived by default"):
        assert source[0].includeDerived is False

    with subtests.test():
        assert expected_output_filename_b == source[1].output


def test_get_tile_files_with_include_derived(subtests: SubTests) -> None:
    file_source = '[{"output": "tile_name","input": ["file_a.tiff", "file_b.tiff"], "includeDerived": true}]'
    expected_output_filename = "tile_name"
    expected_input_filenames = ["file_a.tiff", "file_b.tiff"]

    source: list[TileFiles] = get_tile_files(file_source)
    with subtests.test():
        assert expected_output_filename == source[0].output

    with subtests.test():
        assert expected_input_filenames == source[0].inputs

    with subtests.test():
        assert source[0].includeDerived is True


def test_parse_list() -> None:
    str_list = "Auckland Council; Toitū Te Whenua Land Information New Zealand;Nelson Council;"
    list_parsed = parse_list(str_list)
    assert list_parsed == ["Auckland Council", "Toitū Te Whenua Land Information New Zealand", "Nelson Council"]


def test_parse_list_empty() -> None:
    # pylint: disable=use-implicit-booleaness-not-comparison
    list_parsed = parse_list("")
    assert list_parsed == []


def test_parse_list_drops_whitespace_only_entries() -> None:
    # A whitespace-only entry between two values must not leak into the output.
    list_parsed = parse_list("Auckland Council; ; Nelson Council")
    assert list_parsed == ["Auckland Council", "Nelson Council"]


def test_coalesce_multi_no_single() -> None:
    multi_items = "foo; bar baz"
    single_item = ""
    coalesced_list = coalesce_multi_single(multi_items, single_item)
    assert coalesced_list == ["foo", "bar baz"]


def test_coalesce_single_no_multi() -> None:
    multi_items = ""
    single_item = "foo"
    coalesced_list = coalesce_multi_single(multi_items, single_item)
    assert coalesced_list == ["foo"]


def test_coalesce_nothing() -> None:
    # pylint: disable=use-implicit-booleaness-not-comparison
    multi_items = ""
    single_item = ""
    coalesced_list = coalesce_multi_single(multi_items, single_item)
    assert coalesced_list == []


def test_valid_date_empty_string() -> None:
    assert valid_date("") is None


def test_valid_date_valid_string() -> None:
    assert isinstance(valid_date("2024-11-21"), datetime)


def test_valid_date_invalid_string() -> None:
    with raises(Exception) as e:
        valid_date("foo")
    assert str(e.value) == "not a valid date: foo"


def test_get_geometry_from_geojson_feature() -> None:
    geom = MultiPolygon(
        [[[(175.326912, -41.66861622), (175.33531971, -41.67266055), (175.3351674, -41.6684487), (175.326912, -41.66861622)]]]
    )
    geojson: dict[str, Any] = {
        "type": "FeatureCollection",
        "name": "foo",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": [
            {
                "type": "Feature",
                "properties": {"Id": 0},
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [175.326912, -41.66861622],
                                [175.33531971, -41.67266055],
                                [175.3351674, -41.6684487],
                                [175.326912, -41.66861622],
                            ]
                        ]
                    ],
                },
            }
        ],
    }
    assert get_geometry_from_geojson_feature(geojson["features"][0], "/tmp/test/test.geojson") == geom


def test_get_geometry_from_invalid_geojson_feature() -> None:
    geojson = {
        "foo": "bar",
    }
    with raises(Exception) as e:
        get_geometry_from_geojson_feature(geojson, "/tmp/test/test.geojson")
    assert str(e.value) == "The supplied GeoJSON feature does not contain a valid geometry: /tmp/test/test.geojson"


def test_get_geometry_from_empty_geojson_feature_geom() -> None:
    geojson: dict[str, Any] = {
        "type": "FeatureCollection",
        "name": "foo",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": [
            {
                "type": "Feature",
                "properties": {"Id": 0},
                "geometry": {},
            }
        ],
    }
    with raises(Exception) as e:
        get_geometry_from_geojson_feature(geojson["features"][0], "/tmp/test/test.geojson")
    assert str(e.value) == "The supplied GeoJSON feature does not contain a valid geometry: /tmp/test/test.geojson"


def test_get_non_empty_features() -> None:
    geojson: dict[str, Any] = {
        "type": "FeatureCollection",
        "name": "foo",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": [],
    }
    with raises(Exception) as e:
        get_non_empty_features(geojson, "/tmp/test/test.geojson")
    assert str(e.value) == "Supplied GeoJSON has no features: /tmp/test/test.geojson"


def test_get_non_empty_features_valid_feature_collection() -> None:
    geojson: dict[str, Any] = {
        "type": "FeatureCollection",
        "name": "foo",
        "features": [
            {
                "type": "Feature",
                "geometry": {},
            },
            {
                "type": "Feature",
                "geometry": {},
            },
        ],
    }
    features = get_non_empty_features(geojson, "/tmp/test/test.geojson")
    assert len(features) == 2


def test_get_non_empty_features_single_feature() -> None:
    geojson: dict[str, Any] = {
        "type": "Feature",
        "geometry": {},
    }
    features = get_non_empty_features(geojson, "/tmp/test/test.geojson")
    assert len(features) == 1
    assert features[0]["type"] == "Feature"


def test_str_to_positive_int_returns_int_when_value_is_positive() -> None:
    assert str_to_positive_int("5") == 5


def test_str_to_positive_int_raises_when_value_is_not_an_integer() -> None:
    with raises(ArgumentTypeError) as e:
        str_to_positive_int("foo")
    assert str(e.value) == "'foo' is not a valid integer"


def test_str_to_positive_int_raises_when_value_is_zero() -> None:
    with raises(ArgumentTypeError) as e:
        str_to_positive_int("0")
    assert str(e.value) == "must be >= 1"


def test_str_to_positive_int_raises_when_value_is_negative() -> None:
    with raises(ArgumentTypeError) as e:
        str_to_positive_int("-1")
    assert str(e.value) == "must be >= 1"


def test_str_to_bool_returns_true_when_value_is_true() -> None:
    assert str_to_bool("true") is True


def test_str_to_bool_returns_false_when_value_is_false() -> None:
    assert str_to_bool("false") is False


def test_str_to_bool_raises_when_value_is_not_a_boolean() -> None:
    with raises(ArgumentTypeError) as e:
        str_to_bool("yes")
    assert "yes" in str(e.value)


def test_str_to_list_or_none_returns_none_when_value_is_empty() -> None:
    assert str_to_list_or_none("") is None


def test_str_to_list_or_none_returns_two_decimals_when_value_has_two_items() -> None:
    assert str_to_list_or_none("2,4") == [Decimal("2"), Decimal("4")]


def test_str_to_list_or_none_raises_when_value_has_wrong_length() -> None:
    with raises(ArgumentTypeError) as e:
        str_to_list_or_none("2,4,6")
    assert "exactly 2 values" in str(e.value)


def test_str_to_list_or_none_raises_when_value_is_not_numeric() -> None:
    with raises(ArgumentTypeError) as e:
        str_to_list_or_none("foo,4")
    assert "must be numeric" in str(e.value)


def test_str_to_gsd_returns_decimal_when_value_is_valid() -> None:
    assert str_to_gsd("0.3") == Decimal("0.3")


def test_str_to_gsd_raises_when_value_is_not_a_valid_decimal() -> None:
    with raises(ArgumentTypeError) as e:
        str_to_gsd("foo")
    assert str(e.value) == "'foo' is not a valid GSD value"
