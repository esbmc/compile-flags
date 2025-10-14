# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**compile-flags** is a multi-language compilation flags detector tool written in Python. The project uses:
- **Hatch** as the build system and project manager
- **Python 3.12+** as the minimum required version
- **pydantic-settings** for configuration management
- **AGPL-3.0** license

## Development Commands

### Package Management
```bash
# Install in development mode
hatch shell

# Build the package
hatch build
```

### Testing
```bash
# Run tests (when test framework is added)
hatch test

# Run tests with coverage
hatch test --cover
```

### Type Checking
```bash
# Run mypy type checker
hatch run types:check

# Type check specific files
hatch run types:check compile_flags/module.py
```

## Project Structure

- `compile_flags/` - Main package source code
  - `__about__.py` - Version information
  - `__init__.py` - Package initialization
- `tests/` - Test suite (pytest-based)
- `pyproject.toml` - Project configuration and dependencies

## Important Notes

- The project uses modern Python type hints (e.g., `dict` instead of `Dict`, `| None` instead of `Optional`)
- Version is managed in `compile_flags/__about__.py` (note: pyproject.toml incorrectly references `src/compile_flags/__about__.py`)
- Coverage configuration excludes `__about__.py` from coverage reports
- All source files include SPDX license headers (MIT for code files)
- Use modern Python annotations, for example, use "| None" instead of "Optional".
- Type annotate everything, including variables, function arguments, and function returns.