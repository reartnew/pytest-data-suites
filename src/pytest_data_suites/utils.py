# MIT License
#
# Copyright (c) 2022 Artem Novikov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Class-based pytest parametrization"""

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