# SPDX-FileCopyrightText: 2025-present Yiannis Charalambous <yiannis128@hotmail.com>
#
# SPDX-License-Identifier: AGPL-3.0

"""Handles loading from command line args."""

import logging
import os
from pathlib import Path
import sys

import structlog
from pydantic import AliasChoices, DirectoryPath, Field, FilePath, PrivateAttr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _alias_choice(value: str) -> AliasChoices:
    """
    Create aliases for config fields to work with multiple sources.

    Args:
        value: The field name

    Returns:
        AliasChoices with field name, dashed version, and env var version
    """
    return AliasChoices(
        value,  # exact field name for direct matching
        value.replace("_", "-"),  # dashed alias for CLI
        f"COMPILE_FLAGS_{value.replace('-', '_').upper()}",  # prefixed env var alias
    )


def configure_logging(log_level: int) -> None:
    """
    Configure structlog with appropriate processors and log level.

    Args:
        log_level: The logging level to use
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        stream=sys.stdout,
    )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.dev.ConsoleRenderer(colors=True),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )


class Config(BaseSettings):
    """Configuration for compile-flags tool."""

    # override from BaseSettings
    model_config = SettingsConfigDict(
        case_sensitive=False,
        cli_parse_args=True,
    )

    output_file: FilePath | None = Field(
        default=None,
        validation_alias=_alias_choice("output_file"),
        description="Output file path for compilation flags",
    )

    language: str | None = Field(
        default=None,
        validation_alias=_alias_choice("language"),
        description="Programming language to detect flags for "
        "(e.g., c, cpp, rust). Will try and automatically detect if unspecified",
    )

    build_dir: DirectoryPath = Field(
        default=Path(os.getcwd()),
        validation_alias=_alias_choice("build_dir"),
        description="Build directory to analyze",
    )

    @computed_field
    @property
    def log_level(self) -> int:
        """The current log level."""
        return logging.getLogger().getEffectiveLevel()

    @computed_field
    @property
    def log_level_name(self) -> str:
        """The current log level name."""
        return logging.getLevelName(self.log_level)

