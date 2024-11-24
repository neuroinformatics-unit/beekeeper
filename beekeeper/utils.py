import pathlib as pl

import pandas as pd
import yaml


def df_from_metadata_yaml_files(
    parent_dir: str, metadata_fields_dict: dict
) -> pd.DataFrame:
    """Build a dataframe from all the metadata.yaml files in the input parent
    directory.

    If there are no metadata.yaml files in the parent directory, make a
    dataframe with the columns as defined in the metadata fields
    description and empty (string) fields


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
        for f in pl.Path(parent_dir).iterdir()
        if str(f).endswith(".metadata.yaml")
    ]

    # If there are no metadata (yaml) files:
    #  build dataframe from metadata_fields_dict
    if not list_metadata_files:
        return pd.DataFrame.from_dict(
            {c: [""] for c in metadata_fields_dict.keys()},
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
    """Set a metadata table row's checkbox to True
    when its data is edited.

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
        key = pl.Path(row[app_storage["metadata_key_field_str"]]).stem

        # write each row to yaml
        yaml_filename = key + ".metadata.yaml"
        with open(
            pl.Path(app_storage["videos_dir_path"]) / yaml_filename, "w"
        ) as yamlf:
            yaml.dump(row, yamlf, sort_keys=False)

    return


def read_and_restructure_DLC_dataframe(
    h5_file: str,
) -> pd.DataFrame:
    """Read and reorganise columns in DLC dataframe
    The columns in the DLC dataframe as read from the h5 file are
    reorganised to more closely match a long format.

    The original columns in the DLC dataframe are multi-level, with
    the following levels:
    - scorer: if using the output from a model, this would be the model_str
      (e.g. 'DLC_resnet50_jwasp_femaleandmaleSep12shuffle1_1000000').
    - bodyparts: the keypoints tracked in the animal (e.g., head, thorax)
    - coords: x, y, likelihood

    We reshape the dataframe to have a single level along the columns,
    and the following columns:
    - model_str: string that characterises the model used
      (e.g. 'DLC_resnet50_jwasp_femaleandmaleSep12shuffle1_1000000')
    - frame: the (zero-indexed) frame number the data was tracked at.
      This is inherited from the index of the DLC dataframe.
    - bodypart: the keypoints tracked in the animal (e.g., head, thorax).
      Note we use the singular, rather than the plural as in DLC.
    - x: x-coordinate of the bodypart tracked.
    - y: y-coordinate of the bodypart tracked.
    - likelihood: likelihood of the estimation provided by the model
    The data is sorted by bodypart, and then by frame.

    Parameters
    ----------
    h5_file : str
        path to the input h5 file
    Returns
    -------
    pd.DataFrame
        a dataframe with the h5 file data, and the columns as specified above
    """
    # TODO: can this be less hardcoded?
    # TODO: check with multianimal dataset!

    # read h5 file as a dataframe
    df = pd.read_hdf(h5_file)

    # determine if model is multianimal
    is_multianimal = "individuals" in df.columns.names

    # assuming the DLC index corresponds to frame number!!!
    # TODO: can I check this?
    # frames are zero-indexed
    df.index.name = "frame"

    # stack scorer and bodyparts levels from columns to index
    # if multianimal, also column 'individuals'
    columns_to_stack = ["scorer", "bodyparts"]
    if is_multianimal:
        columns_to_stack.append("individual")
    df = df.stack(level=columns_to_stack)  # type: ignore
    # Not sure why mypy complains, list of labels is allowed
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.stack.html
    # ignoring for now

    # reset index to remove 'frame','scorer' and 'bodyparts'
    # if multianimal, also remove 'individuals'
    df = df.reset_index()  # removes all levels in index by default

    # reset name of set of columns and indices
    # (to remove columns name = 'coords')
    df.columns.name = ""
    df.index.name = ""

    # rename columns
    # TODO: if multianimal, also 'individuals'
    columns_to_rename = {
        "scorer": "model_str",
        "bodyparts": "bodypart",
    }
    if is_multianimal:
        columns_to_rename["individuals"] = "individual"
    df.rename(
        columns=columns_to_rename,
        inplace=True,
    )

    # reorder columns
    list_columns_in_order = [
        "model_str",
        "frame",
        "bodypart",
        "x",
        "y",
        "likelihood",
    ]
    if is_multianimal:
        # insert 'individual' in second position
        list_columns_in_order.insert(1, "individual")
    df = df[list_columns_in_order]

    # sort rows by bodypart and frame
    # if multianimal: sort by individual first
    list_columns_to_sort_by = ["bodypart", "frame"]
    if is_multianimal:
        list_columns_to_sort_by.insert(0, "individual")
    df.sort_values(by=list_columns_to_sort_by, inplace=True)  # type: ignore

    # reset dataframe index
    df = df.reset_index(drop=True)

    return df  # type: ignore


def get_dataframes_to_combine(
    list_selected_videos: list,
    slider_start_end_labels: list,
    app_storage: dict,
) -> list:
    """Create list of dataframes to export as one

    Parameters
    ----------
    list_selected_videos : list
        list of videos selected in the table
    slider_start_end_labels : list
        labels for the slider start and end positions
    app_storage : dict
        data held in temporary memory storage,
        accessible to all tabs in the app

    Returns
    -------
    list_df_to_export : list
        list of dataframes to concatenate
        before exporting
    """
    # TODO: allow model_str to be a list?
    # (i.e., consider the option of different models being used)

    # List of h5 files corresponding to
    # the selected videos
    list_h5_file_paths = [
        pl.Path(app_storage["config"]["pose_estimation_results_path"])
        / (pl.Path(vd).stem + app_storage["config"]["model_str"] + ".h5")
        for vd in list_selected_videos
    ]

    # Read the dataframe for each video and h5 file
    list_df_to_export = []
    for h5, video in zip(list_h5_file_paths, list_selected_videos):
        # Get the metadata file for this video
        # (built from video filename)
        yaml_filename = pl.Path(app_storage["config"]["videos_dir_path"]) / (
            pl.Path(video).stem + ".metadata.yaml"
        )
        with open(yaml_filename, "r") as yf:
            metadata = yaml.safe_load(yf)

        # Extract frame start/end using info from slider
        frame_start_end = [metadata["Events"][x] for x in slider_start_end_labels]

        # -----------------------------

        # Read h5 file and reorganise columns
        # TODO: I assume index in DLC dataframe represents frame number
        # (0-indexed) -- check this with download from ceph and ffmpeg
        df = read_and_restructure_DLC_dataframe(h5)

        # Extract subset of rows based on events slider
        # (frame numbers from slider, both inclusive)
        df = df.loc[
            (df["frame"] >= frame_start_end[0]) & (df["frame"] <= frame_start_end[1]),
            :,
        ]

        # -----------------------------
        # Add video file column
        # (insert after model_str)
        df.insert(1, "video_file", video)

        # Add ROI per frame and bodypart,
        # if ROIs defined for this video
        # To set hierarchy of ROIs:
        # - Start assigning from the smallest,
        # - only set ROI if not previously defined
        # TODO: Is there a better approach?
        df["ROI_tag"] = ""  # initialize ROI column with empty strings
        if "ROIs" in metadata:
            # Extract ROI paths for this video if defined
            # TODO: should I do case insensitive?
            # if "rois" in [ky.lower() for ky in metadata.keys()]:
            ROIs_as_polygons = {
                el["name"]: svg_path_to_polygon(el["path"]) for el in metadata["ROIs"]
            }
            df = add_ROIs_to_video_dataframe(df, ROIs_as_polygons, app_storage)

        # Add Event tags if defined
        # - if no event is defined for that frame: empty str
        # - if an event is defined for that frame: event_tag
        df["event_tag"] = ""
        if "Events" in metadata:
            for event_str in metadata["Events"].keys():
                event_frame = metadata["Events"][event_str]
                df.loc[df["frame"] == event_frame, "event_tag"] = event_str

        # Append to list
        list_df_to_export.append(df)

    return list_df_to_export
    return list_df_to_export
