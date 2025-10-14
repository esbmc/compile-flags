# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**compile-flags** is a multi-language compilation flags detector tool written in Python. The project uses:
- **Hatch** as the build system and project manager
- **Python 3.12+** as the minimum required version
- **pydantic-settings** for configuration management
- **structlog** for structured logging
- **AGPL-3.0** license

## Development Commands

### Running the Application
```bash
# Run with hatch (preferred method)
hatch run compile-flags [options]

# Examples:
hatch run compile-flags --help
hatch run compile-flags -v              # INFO level logging
hatch run compile-flags -vv             # DEBUG level logging
hatch run compile-flags -vv -l rust -b /path/to/build

# Run directly via Python module
hatch run python -m compile_flags [options]
```

### Package Management
```bash
# Install in development mode
hatch shell

# Build the package
hatch build
```

### Type Checking
```bash
# Run mypy type checker
hatch run types:check

# Type check specific files
hatch run types:check compile_flags/module.py
```

## Architecture

### Configuration System
The application uses a hybrid approach combining **argparse** for CLI parsing with **Pydantic Settings** for configuration management:

1. **CLI Parsing (`__main__.py`)**: Uses argparse with `action="count"` to support `-v`, `-vv`, `-vvv` verbosity levels
2. **Configuration Model (`config.py`)**: Pydantic `BaseSettings` model that:
   - Validates all configuration values with type safety
   - Uses `@model_validator` to compute `log_level` from `verbose` count
   - Integrates with `CliApp.run()` pattern via `CliSettingsSource`

### Logging System
- **structlog** for structured logging with colored console output
- Log levels mapped from verbosity: 0=WARNING, 1=INFO, 2+=DEBUG
- Configuration in `config.py:configure_logging()`
- All log messages include structured key-value pairs for better debugging

### Entry Point Flow
```
__main__.py:parse_args()
  → CliApp.run(Config, cli_settings_source=...)
  → config.py:compute_log_level() (model_validator)
  → __main__.py:configure_logging()
  → Application logic with structured logging
```

## Code Style

- Use modern Python type hints: `dict` not `Dict`, `| None` not `Optional`
- Type annotate everything: variables, function arguments, and return types
- All source files must include SPDX license headers (MIT for code files)
- Version is managed in `compile_flags/__about__.py`

## Important Notes

- The hatch script at `pyproject.toml:39` uses `{args}` to pass CLI arguments through
- When adding CLI arguments, update both `parse_args()` in `__main__.py` and the corresponding field in `Config` model
- The `Config` model has `case_sensitive=False` for environment variable support
- Environment variables can override defaults using `COMPILE_FLAGS_` prefix
- Use modern Python type hints: `dict` not `Dict`, `| None` not `Optional`
- Type annotate everything: variables, function arguments, and return types
- All source files must include SPDX license headers (AGPL-3.0 for source files)
- Version is managed in `compile_flags/__about__.py`