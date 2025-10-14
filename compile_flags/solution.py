# SPDX-FileCopyrightText: 2025-present Yiannis Charalambous <yiannis128@hotmail.com>
#
# SPDX-License-Identifier: AGPL-3.0

from pydantic import BaseModel, Field, FilePath


class SourceFile(BaseModel):
    """Represents a generic source file."""

    path: FilePath = Field(description="The file path of this source file.")

    @property
    def dependencies(self) -> list[FilePath]:
        """Gets the deps of this source file. Needs to be overwritten."""
        return []


class Solution(BaseModel):
    """Represents the codebase."""

    source_files: dict[FilePath, SourceFile] = Field(
        default_factory=dict, description="The list of source files."
    )
