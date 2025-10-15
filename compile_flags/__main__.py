# SPDX-FileCopyrightText: 2025-present Yiannis Charalambous <yiannis128@hotmail.com>
#
# SPDX-License-Identifier: AGPL-3.0

"""Entry point of compile-flags."""

import argparse
import logging

import structlog
from pydantic_settings import CliApp, CliSettingsSource

from compile_flags.config import Config, configure_logging


def create_parser() -> argparse.ArgumentParser:
    """Create argparse parser with custom arguments."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="compile-flags",
        description="Multi-language compilation flags detector tool",
    )

    # Only add custom arguments that need special handling
    # CliSettingsSource will automatically add all other Config fields
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (use -v for INFO, -vv for DEBUG, -vvv for maximum verbosity)",
    )

    return parser


def main() -> None:
    """Main entry point for compile-flags CLI."""
    # Create parser with custom arguments
    parser: argparse.ArgumentParser = create_parser()

    # Parse verbose level before Pydantic CLI parsing
    args, _ = parser.parse_known_args()
    verbose: int = args.verbose if hasattr(args, "verbose") else 0

    # Map verbose count to log level
    if verbose == 0:
        log_level = logging.WARNING
    elif verbose == 1:
        log_level = logging.INFO
    else:  # 2+
        log_level = logging.DEBUG

    # Configure logging before loading config, will also update in the config.
    configure_logging(log_level)

    # Create custom CLI settings source using our argparse parser
    # This will automatically add all non-excluded Config fields to the parser
    cli_settings: CliSettingsSource = CliSettingsSource(
        Config,
        cli_parse_args=True,
        root_parser=parser,
        cli_implicit_flags=True,
    )

    # Use CliApp.run with custom CLI settings source
    config: Config = CliApp.run(Config, cli_settings_source=cli_settings)

    # Get structured logger
    log: structlog.stdlib.BoundLogger = structlog.get_logger()

    # Log configuration
    log.debug("Configuration loaded", **config.model_dump(mode="python"))
    log.info("Starting compilation flags detection", build_dir=config.build_dir)

    print("TODO")


if __name__ == "__main__":
    main()
