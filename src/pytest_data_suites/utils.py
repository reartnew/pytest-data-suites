"""Auxiliary utilities"""

from __future__ import annotations

import re
from typing import (
    Pattern,
)

__all__ = [
    "string_to_kebab_case",
]

_NON_CAP_REPLACER: Pattern = re.compile(r"(.)([A-Z][a-z]+)")
_CAP_REPLACER: Pattern = re.compile(r"([a-z0-9])([A-Z])")
_DASH_REPLACEMENT: str = r"\1-\2"


def string_to_kebab_case(string: str) -> str:
    """Transform a the given string to kebab-case.
    Double-replace to transform names with many capital letter in a row"""
    return "-".join(
        _CAP_REPLACER.sub(_DASH_REPLACEMENT, _NON_CAP_REPLACER.sub(_DASH_REPLACEMENT, chunk)).lower()
        for chunk in re.split(r"[-_]+", string)
    )
