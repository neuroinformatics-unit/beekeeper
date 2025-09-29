# Contributing to `beekeeping`

## Introduction

**Contributors to `beekeeping` are absolutely encouraged**, whether to fix a bug, develop a new feature, or improve the documentation.
If you're unsure about any part of the contributing process, please get in touch. It's best to reach out in public, e.g. by opening an issue so that others can benefit from the discussion.

## Contributing code

### Creating a development environment

It is recommended to use [conda](https://docs.conda.io/en/latest/) to install a development environment for
`beekeeping`. Once you have `conda` installed, create and activate a `conda` environment for development with the following commands:

```sh
conda create -n beekeeping-dev -c conda-forge python=3.12
conda activate beekeeping-dev
```

To install the development version of `beekeeping`, clone the GitHub repository, and then run from the root of the repository:

```sh
pip install -e '.[dev]'
```

This will install the package with all the development dependencies.


### Development workflow
We follow the [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow):
1. Create a [fork](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project) of the `beekeeping` repository.

2. Clone the forked repository to your local machine and change directories
    ```
    git clone https://github.com/your-username/beekeeping.git
    cd beekeeping
    ```

3. Set the upstream remote to the base `beekeeping` repository:
    ```
    git remote add upstream https://github.com/neuroinformatics-unit/beekeeping.git
    ```

4. If you haven't already, create a development environment and install the `beekeeping` package in development mode (see [creating a development environment](#creating-a-development-environment)).

5. We use [pre-commit hooks](https://pre-commit.com/) to ensure a consistent formatting style. They are defined in the `.pre-commit-config.yaml` file. Install the pre-commit hooks by running:
    ```
    pre-commit install
    ```
    Upon committing, the hooks will run and try to automatically format the code according to the predefined rules. If a problem cannot be auto-fixed, the corresponding tool will provide
    information on what the issue is and how to fix it. Please ensure all hooks pass before committing.

6. Now create a new branch in your fork, edit the code or documentation, and commit your changes.

7. Submit your changes via a pull request, following the [pull requests](#pull-requests) guidelines.

These guidelines are based on the [napari guide](https://napari.org/dev/developers/contributing/dev_install.html#dev-installation).



## Development guidelines

### Pull requests

In all cases, please submit code to the main repository via a pull request. We adhere to the following conventions:

- Please submit _draft_ pull requests as early as possible to allow for discussion.
- One approval of a PR (by a repo owner) is enough for it to be merged.
- Unless someone approves the PR with optional comments, the PR is immediately merged by the approving reviewer.
- Ask for a review from someone specific if you think they would be a particularly suited reviewer


### Testing

We use [pytest](https://docs.pytest.org/en/latest/) for testing, and our integration tests require Google chrome or chromium and a compatible `chromedriver`.
Please try to ensure that all functions are tested, including both unit and integration tests.
Write your test methods and classes in the `test` folder.

#### Integration tests with chrome

The integration tests start a server and browse with chrome(ium),
so you will need to download and install Google chrome or chromium (if you don't already use one of them).
You will then need to download a [compatible version of `chromedriver`](https://chromedriver.chromium.org/downloads).
Depending on your OS you may also need to ***trust*** the executable.

<details>
<summary>Ubuntu</summary>

Installing chromium and chromedriver is a one-liner (tested in Ubuntu 20.04 and 22.04).

```sh
sudo apt install chromium-chromedriver
pytest # in the root of the repository
```

</details>

<details>
<summary>MacOS</summary>
There is also a [homebrew cask](https://formulae.brew.sh/cask/chromedriver) for `chromedriver` so instead of going to the web and downloading you should be able to:

```sh
brew install chromedriver
brew info chromedriver
```
And take note of the installation path.
(It's probably something like `/opt/homebrew/Caskroom/chromedriver/<version>`).

However you obtained `chomedriver`, you can trust the executable via the security settings and/or keychain GUI or just:

```sh
cd /place/where/your/chromedriver/is
xattr -d com.apple.quarantine chromedriver
```

Once downloaded, make sure the `chromedriver` binary in your `PATH` and check that you can run the integration tests.

```sh
export PATH=$PATH:/place/where/your/chromedriver/is/chromedriver
pytest # in the root of the repository
```

</details>

<details>
<summary>Windows</summary>

For Windows, be sure to download the ``chromedriver_win32.zip`` file, extract the executable, and it's probably easiest to simply place it in the directory where you want to run ``pytest``.

</details>

It's a good idea to test locally before pushing. Pytest will run all tests and also report test coverage.

### Continuous integration
All pushes and pull requests will be built by [GitHub actions](https://docs.github.com/en/actions). This will usually include linting, testing and deployment.

A GitHub actions workflow (`.github/workflows/test_and_deploy.yml`) has been set up to run (on each commit/PR):
* Linting checks (pre-commit).
* Testing (only if linting checks pass)
* Release to PyPI (only if a git tag is present and if tests pass). Requires `TWINE_API_KEY` from PyPI to be set in repository secrets.

### Versioning and releases
We use [semantic versioning](https://semver.org/), which includes `MAJOR`.`MINOR`.`PATCH` version numbers:

* PATCH = small bugfix
* MINOR = new feature
* MAJOR = breaking change

We use [`setuptools_scm`](https://github.com/pypa/setuptools_scm) to automatically version `beekeeping`. It has been pre-configured in the `pyproject.toml` file. `setuptools_scm` will automatically infer the version using git. To manually set a new semantic version, create a tag and make sure the tag is pushed to GitHub. Make sure you commit any changes you wish to be included in this version. E.g. to bump the version to `1.0.0`:

```sh
git add .
git commit -m "Add new changes"
git tag -a v1.0.0 -m "Bump to version 1.0.0"
git push --follow-tags
```

Pushing a tag to GitHub triggers the package's deployment to PyPI. The version number is automatically determined from the latest tag on the `main` branch.

## Contributing documentation

The documentation is hosted via [GitHub pages](https://pages.github.com/) at [beekeeping.neuroinformatics.dev](https://beekeeping.neuroinformatics.dev/). Its source files are located in the `docs` folder of this repository.

Source files are written in either [reStructuredText](https://docutils.sourceforge.io/rst.html) or [markdown](https://myst-parser.readthedocs.io/en/stable/syntax/typography.html).
The `index.rst` file corresponds to the main page of the documentation website. Other `.rst`  or `.md` files are included in the main page via the `toctree` directive.

We use [Sphinx](https://www.sphinx-doc.org/en/master/) and the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html) to build the source files into html output. This is handled by a GitHub actions workflow (`.github/workflows/publish_docs.yml`) which is triggered whenever changes are pushed to the `main` branch. The workflow builds the html output files and sends them to a `gh-pages` branch.

### Editing the documentation

To edit the documentation (`.md` or `.rst` in the `docs` folder), first follow the usual [development workflow](#development-workflow) steps.

If you create a new documentation source file (e.g. `my_new_file.md` or `my_new_file.rst`), you will need to add it to the `toctree` directive in `index.rst` for it to be included in the documentation website:

```rst
.. toctree::
   :maxdepth: 2

   existing_file
   my_new_file
```

### Building the documentation locally
We recommend that you build and view the documentation website locally, before you push it.
To do so, first install the requirements for building the documentation:
```sh
pip install -r docs/requirements.txt
```

Then, from the root of the repository, run:
```sh
sphinx-build docs/source docs/build
```

You can view the local build by opening `docs/build/index.html` in a browser.
To refresh the documentation, after making changes, remove the `docs/build` folder and re-run the above command:

```sh
rm -rf docs/build
sphinx-build docs/source docs/build
```

## Overview of the codebase

*Generated by Claude*

### Architecture
```
beekeeping/
├── app.py              # Main Dash app initialization
├── pages/              # Page components
│   ├── home.py         # Upload interface
│   └── metadata.py     # Table interface
├── callbacks/          # Event handlers
│   ├── home.py         # Config upload logic
│   └── metadata.py     # Table operations
└── utils.py            # Data processing utilities
```

### Key components

#### **1. Application bootstrap (`app.py`)**
```python
# Multi-page Dash app with Bootstrap theming
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Fixed sidebar + dynamic content area layout
app.layout = html.Div([sidebar, content, storage])

# Register callbacks from modules
home.get_callbacks(app)
metadata.get_callbacks(app)
```

#### **2. Session storage pattern**
- **Storage component**: `dcc.Store(id="session-storage")` maintains state across pages
- **Data structure**:
  ```python
  {
      "config": {...},           # Project configuration
      "metadata_fields": {...}   # Field definitions and validation
  }
  ```

#### **3. Callback architecture**
**Home page callbacks:**
- `save_input_config_to_storage()`: Processes uploaded YAML, loads metadata fields, stores in session

**Metadata page callbacks:**
- `create_metadata_table_and_buttons()`: Builds table from YAML files or shows error
- `add_rows()`: Handles manual and automatic row addition
- `modify_rows_selection()`: Manages selection, editing, and export
- `generate_yaml_files_from_spreadsheet()`: Processes uploaded spreadsheets

### Data flow

#### **Configuration loading**
1. User uploads project_config.yaml
2. Callback parses YAML and reads metadata_fields.yaml
3. Data stored in session storage
4. Other callbacks access via app_storage parameter


#### **Metadata table generation**
1. utils.df_from_metadata_yaml_files() scans directory
2. Reads all *.metadata.yaml files
3. Creates pandas DataFrame
4. create_metadata_table_component_from_df() builds Dash table


#### **YAML export process**
1. User selects rows and clicks export
2. modify_rows_selection() callback triggers
3. utils.export_selected_rows_as_yaml() processes selection
4. Writes individual .metadata.yaml files to videos directory
