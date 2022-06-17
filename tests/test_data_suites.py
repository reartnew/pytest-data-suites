# -*- coding: utf-8 -*-
"""DataSuite decorator tests"""

from typing import List

import pytest

from .cases import StringTransformationDataSuite


@StringTransformationDataSuite.parametrize
def test_dummy(initial: str, expected: str) -> None:
    """Simple parameters check"""
    assert isinstance(initial, str)
    assert isinstance(expected, str)


@pytest.mark.last
def test_parametrized_tests_presence(request: pytest.FixtureRequest) -> None:
    """Validate correct tests parametrization"""
    dummy_test_names: List[str] = [
        test.name
        for test in request.session.items
        if getattr(test, "originalname", None) == "test_dummy"
    ]
    assert len(dummy_test_names) == 7
