[![License](https://img.shields.io/badge/License-BSD_3--Clause-orange.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![CI](https://img.shields.io/github/actions/workflow/status/SainsburyWellcomeCentre/beekeeping/test_and_deploy.yml?label=CI)](https://github.com/neuroinformatics-unit/beekeeping/actions)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# `beekeeping` 🐝
Manage video metadata for animal behaviour experiments.

## Overview

`beekeeping` is a web-based dashboard built with [Dash-Plotly](https://dash.plotly.com/) for managing video metadata in animal behaviour experiments. It provides an intuitive interface for creating, editing, and organizing metadata files associated with experimental videos.

**Key Features:**
- Upload and manage project configurations
- Interactive metadata table with editing capabilities
- Bulk import from spreadsheets (CSV/Excel)
- Automatic detection of videos missing metadata
- Export metadata as YAML files
- Responsive web interface with Bootstrap theming

It is based on an earlier codebase called [WAZP](https://sainsburywellcomecentre.github.io/WAZP/), but focuses specifically on metadata management.

## Installation

Install `beekeeping` inside a [conda](https://docs.conda.io/en/latest/) environment:

```sh
conda create -n beekeeping-env -c conda-forge python=3.12
conda activate beekeeping-env
git clone https://github.com/neuroinformatics-unit/beekeeping.git
cd beekeeping
pip install .
```

## Getting Started

1. **Launch the application**
   ```bash
   start-beekeeping
   ```
   The app opens in your browser at `http://localhost:8050`

2. **Upload Project Configuration**
   - Navigate to the **Home** page
   - Upload your `project_config.yaml` file containing:
     ```yaml
     videos_dir_path: /path/to/your/videos
     metadata_fields_file_path: /path/to/metadata_fields.yaml
     metadata_key_field_str: File
     ```

3. **Manage Video Metadata**
   - Navigate to the **Metadata** page to view/edit your video metadata table
   - Each row represents one video file's metadata

### Core Operations

#### **Viewing and Editing Metadata**
- **Browse**: Scroll through the paginated table (25 rows per page)
- **Sort**: Click column headers to sort data
- **Hide/Show columns**: Use column visibility controls
- **Edit**: Click any editable cell to modify values directly
- **Row selection**: Click checkboxes to select rows for batch operations

#### **Adding Missing Videos**
- Click **"Check for missing metadata files"**
- The app scans your videos directory and adds rows for videos without `.metadata.yaml` files
- File extensions supported: `.avi`, `.mp4`

#### **Manual Data Entry**
- Click **"Add empty row"** to create a new metadata entry
- Fill in the fields as needed
- The filename field links to your video file

#### **Batch Operations**
- **Select All/Unselect All**: Mass row selection controls
- **Export Selected**: Click "Export selected rows as yaml" to save `.metadata.yaml` files for selected videos
- **Import from Spreadsheet**: Upload CSV/Excel files to bulk generate metadata files

#### **Spreadsheet Import Process**
1. Prepare your spreadsheet (CSV or Excel) with columns matching your metadata fields
2. Click **"Generate yaml files from spreadsheet"**
3. Upload your file
4. The app will:
   - Match spreadsheet columns to metadata fields
   - Add missing columns with empty values
   - Only process rows with corresponding video files
   - Generate `.metadata.yaml` files in your videos directory
   - Show confirmation with count of files generated

## License

⚖️ [BSD 3-Clause](https://opensource.org/licenses/BSD-3-Clause)
