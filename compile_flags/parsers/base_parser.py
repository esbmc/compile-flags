# SPDX-FileCopyrightText: 2025-present Yiannis Charalambous <yiannis128@hotmail.com>
#
# SPDX-License-Identifier: AGPL-3.0

from pydantic import BaseModel, Field

from compile_flags import Solution


class BaseSolutionParser(BaseModel):
    """Base parser class for analyzing a code base."""

    solution: Solution = Field()


class CLikeParser(BaseSolutionParser):
    """C and C++ based parser."""
