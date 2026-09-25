from typing import Any

import pytest
from geoprocessor_gdal.tile.util import charcodeat


def test_returns_character_code_when_given_valid_arguments() -> None:
    assert charcodeat("A", 0) == 65
    assert charcodeat("ABC", 1) == 66


def test_error_reports_actual_index_type_when_index_is_not_an_int() -> None:
    # Regression test: the error message used to read `type(int)` (the class)
    # instead of the actual type of `index`, misreporting the bad argument.
    bad_index: Any = "0"
    with pytest.raises(Exception, match=r"received <class 'str'> and <class 'str'>"):
        charcodeat("A", bad_index)
