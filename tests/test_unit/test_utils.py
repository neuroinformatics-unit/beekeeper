import glob
import tempfile

import pandas as pd
import pytest
import yaml

from beekeeper.callbacks.metadata import create_metadata_table_component_from_df
from beekeeper.utils import df_from_metadata_yaml_files


@pytest.fixture
def metadata_fields(sample_project) -> dict:
    """Get the metadata dictionary from the sample project for testing."""
    fields_file = sample_project / "metadata_fields.yaml"
    with open(fields_file) as fi:
        metadata_fields = yaml.safe_load(fi)
    return metadata_fields


def test_columns_names_and_nrows_in_df_from_metadata(
    sample_project, metadata_fields
) -> None:
    """Normal operation: test we can read the sample project metadata."""
    df_output = df_from_metadata_yaml_files(sample_project / "videos", metadata_fields)

    fields_from_yaml = set(metadata_fields)
    df_columns = set(df_output.columns)
    diff = fields_from_yaml.symmetric_difference(df_columns)
    # Ignore the "ROIs" column, which is absent from the metadata_fields.yaml
    if diff == {"ROIs"}:
        diff = set()
    assert (
        not diff
    ), f"Metadata fields and df columns differ in the following fields: {diff}"

    glob_pattern = (sample_project / "videos" / "*.yaml").as_posix()
    nfiles = len(glob.glob(glob_pattern))
    nrows, _ = df_output.shape
    assert nrows == nfiles, "Number of rows in df != number of yaml files."


def test_df_from_metadata_yaml_no_metadata(metadata_fields) -> None:
    """
    Test with no metadata files (expect just to create an empty dataframe with
    metadata_fields column headers).
    """
    with tempfile.TemporaryDirectory() as empty_existing_directory:
        df_output = df_from_metadata_yaml_files(
            empty_existing_directory, metadata_fields
        )

    assert df_output.shape == (1, len(metadata_fields))


def test_df_from_metadata_garbage() -> None:
    """Check we don't get metadata for things that don't exist."""
    with pytest.raises(FileNotFoundError):
        df_from_metadata_yaml_files("DIRECTORY_DOESNT_EXIST", dict())

    with tempfile.TemporaryDirectory() as empty_existing_directory:
        df_output = df_from_metadata_yaml_files(empty_existing_directory, dict())
    assert df_output.empty, "There shouldn't be any data in the df."


@pytest.mark.parametrize("key_field", ["File", "Date_start", "Species_name"])
def test_create_metadata_table_component_column_ordering(
    metadata_fields, key_field: str
) -> None:
    """Test metadata table creation orders columns with key field first.

    This test verifies that regardless of the original DataFrame column order,
    the key metadata field specified in the config always appears as the
    first column.

    Parameters
    ----------
    metadata_fields : dict
        Metadata fields fixture
    key_field : str
        The metadata field to use as the key field
    """
    # Create a DataFrame with columns deliberately ordered
    # so key field is NOT first
    data = {
        "File": ["video1.avi", "video2.avi"],
        "Species_name": ["species1", "species2"],
        "Date_start": ["2023-01-01", "2023-01-02"],
        "Date_end": ["2023-01-01", "2023-01-02"],
    }

    # Sort columns to ensure key_field is NOT first
    sorted_columns = sorted(data.keys(), key=lambda x: (x == key_field, x))
    df = pd.DataFrame(data)[sorted_columns]

    # Verify our setup: key field should not be first in the original DataFrame
    assert (
        df.columns[0] != key_field
    ), f"Test setup error: '{key_field}' should not be first in original DataFrame"

    # Create config with the specified key field
    config = {"metadata_key_field_str": key_field, "videos_dir_path": "/fake/path"}

    # Create the table component
    table = create_metadata_table_component_from_df(df, config)

    # Verify that the key field is the first column
    first_column_id = table.columns[0]["id"]
    assert (
        first_column_id == key_field
    ), f"First column should be '{key_field}' but was '{first_column_id}'"

    # Verify all expected columns are present
    column_ids = [col["id"] for col in table.columns]
    expected_columns = ["File", "Species_name", "Date_start", "Date_end"]
    for col in expected_columns:
        assert (
            col in column_ids
        ), f"Column '{col}' not found in table columns: {column_ids}"

    # Verify the key field column is not hideable
    first_column_hideable = table.columns[0]["hideable"]
    assert (
        not first_column_hideable
    ), f"Key field column '{key_field}' should not be hideable"
