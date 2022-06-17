# -*- coding: utf-8 -*-
"""DataSuite decorator tests"""

from typing import TypedDict

from pytest_data_suites import DataSuite

__all__ = [
    "StringTransformationDataSuite",
]


class StringTransformationCase(TypedDict):
    """String-to-string tests namespace"""
    initial: str
    expected: str


class StringTransformationDataSuite(DataSuite):
    """Kebab-case transformation test cases"""
    idempotent_1 = StringTransformationCase(initial="abc", expected="abc")
    idempotent_2 = StringTransformationCase(initial="a-b-c", expected="a-b-c")
    underline_only = StringTransformationCase(initial="a_b_c", expected="a-b-c")
    underline_mixed = StringTransformationCase(initial="a_b-c", expected="a-b-c")
    camel = StringTransformationCase(initial="CamelText", expected="camel-text")
    lower_camel = StringTransformationCase(initial="lowerCamelText", expected="lower-camel-text")
    complex_camel = StringTransformationCase(initial="ComplexXXXCamelText", expected="complex-xxx-camel-text")
