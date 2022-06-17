# -*- coding: utf-8 -*-
"""DataSuite decorator tests"""

from typing import TypedDict, Set

import pytest

from pytest_data_suites import DataSuite


class StringTransformationCase(TypedDict):
    """String-to-string tests namespace"""
    initial: str
    expected: str


class StringReverseDataSuite(DataSuite):
    """Possible cases of string transformation tests"""
    hello = StringTransformationCase(initial="Hello,", expected=",olleH")
    world = StringTransformationCase(initial="world!", expected="!dlrow")


@StringReverseDataSuite.parametrize
def test_reversed(initial: str, expected: str) -> None:
    """Compare reversed strings for fun"""
    assert initial[::-1] == expected


@pytest.mark.last
def test_parametrized_tests_presence(request: pytest.FixtureRequest) -> None:
    """Validate correct tests parametrization"""
    reversed_test_names: Set[str] = {
        test.name
        for test in request.session.items
        if getattr(test, "originalname", None) == "test_reversed"
    }
    assert {"test_reversed[hello]", "test_reversed[world]"} <= reversed_test_names
