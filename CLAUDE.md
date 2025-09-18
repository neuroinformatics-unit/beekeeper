# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This repository contains **`beekeeping`**, a Python-based Dash web application for managing video metadata in animal behaviour experiments. The project is organized as follows:

- `beekeeping/` - Main Python package containing the core application
  - `app.py` - Main Dash application entry point with layout and server startup
  - `pages/` - Dash page components (home.py, metadata.py)
  - `callbacks/` - Dash callback functions (home.py, metadata.py)
  - `utils.py` - Utility functions for data processing
- `tests/` - Test suite (unit and integration tests)
- `docs/` - Sphinx documentation source files

## Development Commands

### Environment Setup
```bash
# Create conda environment (recommended)
conda create -n beekeeping-dev -c conda-forge python=3.12
conda activate beekeeping-dev

# Install for development
pip install -e '.[dev]'

# Install pre-commit hooks
pre-commit install
```
Please double check that pre-commit hooks are running locally and passing before committing.


### Core Commands
```bash
# Start the application
start-beekeeping

# Run tests (requires chromedriver for integration tests)
pytest

# Run tests with coverage
pytest -v --color=yes --cov=beekeeping --cov-report=xml

# Code formatting and linting
pre-commit run      # staged files only
pre-commit run -a   # all files

# Type checking
mypy -p beekeeping

# Build documentation locally
pip install -r docs/requirements.txt
sphinx-build docs/source docs/build
```

### Testing Requirements
- Integration tests require Chrome/Chromium and compatible chromedriver
- Tests use pytest with Dash testing framework
- Use existing fixtures when possible
- Use `tmp_path` fixture for temporary files

## Application Architecture

### Dash Multi-Page Application
- Uses Dash Pages feature (`use_pages=True`) for navigation
- Bootstrap theming via dash-bootstrap-components
- Fixed sidebar navigation with dynamic content area
- Session storage component for maintaining state across pages

### Key Components
- **Main App** (`app.py`): Initializes Dash app, defines layout with sidebar and content areas
- **Pages**: Separate modules for different views (home, metadata)
- **Callbacks**: Event handlers separated by functionality (home.py, metadata.py)
- **Utils**: Data processing functions, particularly for metadata handling

### Data Handling
- YAML-based configuration for metadata fields and project settings
- Project configuration files: project_config.yaml and metadata_fields.yaml

## Configuration Files

### Project Configuration
- `pyproject.toml` - Python package configuration, dependencies, tool settings
- `project_config.yaml` - Application-specific config (videos directory, metadata file paths)
- `metadata_fields.yaml` - Application-specific metadata schema with types, descriptions, validation

### Code Quality Tools
- **ruff**: Linting, import sorting, and formatting (configured in pyproject.toml, line length 79)
- **mypy**: Static type checking with import overrides for external packages
- **pre-commit**: Automated hooks for all code quality checks
