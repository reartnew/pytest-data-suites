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

"""DataSuite definition"""

from __future__ import annotations

import enum
import functools
import inspect
from typing import (
    Any,
    Callable,
    Generator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
)

import pytest

from .utils import string_to_kebab_case

__all__ = [
    "DataSuite",
    "CaseNaming",
]


def _loose_parametrize(argnames: Sequence[str], argvalues: Sequence[Sequence[Any]], ids: Sequence[str]):
    """pytest.mark.parametrize loose wrapper to omit unused arguments """

    def wrapper(func):
        expected_params: Set[str] = set(inspect.signature(func).parameters)
        requested_params_positions: List[int] = [pos for pos, name in enumerate(argnames) if name in expected_params]
        if not requested_params_positions:
            raise ValueError(f"{func} does not use any of: {', '.join(argnames)}")
        return pytest.mark.parametrize(
            argnames=[argnames[k] for k in requested_params_positions],
            argvalues=[[values_list[k] for k in requested_params_positions] for values_list in argvalues],
            ids=ids,
        )(func)

    return wrapper


class CaseNaming(enum.Enum):
    """Valid naming strategies for DataSuite test cases.
    KEBAB_CASE: transform names into kebab-case
    NUMERIC: use test case ordinal number as its name
    """
    KEBAB_CASE = 0
    NUMERIC = 1


class DataSuite:
    """Base class for tests data classes.
    Derivatives may own any number of `dict`-type class properties,
    which would be used to generate test cases via `parametrize` decorator."""

    @classmethod
    def _parametrize(cls, func: Callable, naming: CaseNaming) -> Callable:
        param_names: List[str] = []
        param_values: List[List[str]] = []
        ids: List[str] = []
        known_case_keys: Optional[Set[str]] = None
        for member_index, (member_name, member) in enumerate(cls._get_case_members()):
            # Validate cases uniformity
            current_keys: Set[str] = set(member)
            if known_case_keys not in (None, current_keys):
                raise ValueError(f"Extraordinary case: {member_name!r} (non-uniform parameters)")
            known_case_keys = current_keys
            param_names: List[str] = param_names or sorted(known_case_keys)
            param_values.append([member[param_name] for param_name in param_names])
            ids.append(string_to_kebab_case(member_name) if naming == CaseNaming.KEBAB_CASE else str(member_index))
        return _loose_parametrize(param_names, param_values, ids=ids)(func)

    @classmethod
    def _get_case_members(cls) -> Generator[Tuple[str, dict], None, None]:
        """Iterate over class case-like members"""
        for member_name, member in cls.__dict__.items():
            if isinstance(member, dict):
                yield member_name, member

    @classmethod
    def parametrize(
            cls,
            func: Optional[Callable] = None,
            *,
            naming: CaseNaming = CaseNaming.KEBAB_CASE,
    ) -> Callable:
        """Parameter-injecting decorator.
        :param Callable func: Wrapped test function (commonly passed implicitly)
        :param CaseNaming naming: derived tests naming strategy"""
        if not isinstance(naming, CaseNaming):
            raise ValueError(f"`naming` argument must be of CaseNaming type (caught: {naming!r}")
        return functools.partial(cls._parametrize, naming=naming) \
            if func is None \
            else cls._parametrize(func=func, naming=naming)
