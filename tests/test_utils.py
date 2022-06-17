# -*- coding: utf-8 -*-
"""Utils tests"""

from pytest_data_suites.utils import string_to_kebab_case
from .cases import StringTransformationDataSuite


@StringTransformationDataSuite.parametrize
def test_kebab(initial: str, expected: str) -> None:
    """Validate kebab-case transformations"""
    assert string_to_kebab_case(initial) == expected
