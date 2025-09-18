"""Utility functions for the beekeeping application.

This module contains helper functions for processing metadata files,
dataframe operations, and file management.
"""

from pathlib import Path

import pandas as pd
import yaml


def df_from_metadata_yaml_files(
    parent_dir: str, metadata_fields_dict: dict
) -> pd.DataFrame:
    """Build a dataframe from all metadata.yaml files in the parent directory.

    If there are no metadata.yaml files in the parent directory, make a
    dataframe with the columns as defined in the metadata fields
    description and empty (string) fields.

    Parameters
    ----------
    parent_dir : str
        path to directory with video metadata.yaml files
    metadata_fields_dict : dict
        dictionary with metadata fields descriptions

    Returns
    -------
    pd.DataFrame
        a pandas dataframe in which each row holds the metadata for one video

    """
    # List of metadata files in parent directory
    list_metadata_files = [
        str(f)
        for f in Path(parent_dir).iterdir()
        if str(f).endswith(".metadata.yaml")
    ]

    # If there are no metadata (yaml) files:
    #  build dataframe from metadata_fields_dict
    if not list_metadata_files:
        return pd.DataFrame.from_dict(
            {c: [""] for c in metadata_fields_dict},
            orient="columns",
        )
    # If there are metadata (yaml) files:
    # build dataframe from yaml files
    else:
        list_df_metadata = []
        for yl in list_metadata_files:
            with open(yl) as ylf:
                list_df_metadata.append(
                    pd.DataFrame.from_dict(
                        {
                            k: [v if not isinstance(v, dict) else str(v)]
                            # in the df we pass to the dash table component,
                            # values need to be either str, number or bool
                            for k, v in yaml.safe_load(ylf).items()
                        },
                        orient="columns",
                    )
                )

        return pd.concat(list_df_metadata, ignore_index=True, join="inner")


def set_edited_row_checkbox_to_true(
    data_previous: list[dict], data: list[dict], list_selected_rows: list[int]
) -> list[int]:
    """Set a metadata table row's checkbox to True when its data is edited.

    Parameters
    ----------
    data_previous : list[dict]
        a list of dictionaries holding the previous state of the table
        (read-only)
    data : list[dict]
        a list of dictionaries holding the table data
    list_selected_rows : list[int]
        a list of indices for the currently selected rows

    Returns
    -------
    list_selected_rows : list[int]
        a list of indices for the currently selected rows

    """
    # Compute difference between current and previous table
    # TODO: faster if I compare dicts rather than dfs?
    # (that would be: find the dict in the 'data' list with
    # same key but different value)
    df = pd.DataFrame(data=data)
    df_previous = pd.DataFrame(data_previous)

    df_diff = df.merge(df_previous, how="outer", indicator=True).loc[
        lambda x: x["_merge"] == "left_only"
    ]

    # Update the set of selected rows
    list_selected_rows += [
        i for i in df_diff.index.tolist() if i not in list_selected_rows
    ]

    return list_selected_rows


def export_selected_rows_as_yaml(
    data: list[dict], list_selected_rows: list[int], app_storage: dict
) -> None:
    """Export selected metadata rows as yaml files.

    Parameters
    ----------
    data : list[dict]
        a list of dictionaries holding the table data
    list_selected_rows : list[int]
        a list of indices for the currently selected rows
    app_storage : dict
        data held in temporary memory storage,
        accessible to all tabs in the app

    """
    # Export selected rows
    for row in [data[i] for i in list_selected_rows]:
        # extract key per row
        key = Path(row[app_storage["metadata_key_field_str"]]).stem

        # write each row to yaml
        yaml_filename = key + ".metadata.yaml"
        with open(
            Path(app_storage["videos_dir_path"]) / yaml_filename, "w"
        ) as yamlf:
            yaml.dump(row, yamlf, sort_keys=False)

    return
