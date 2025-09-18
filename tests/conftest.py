import pytest
import yaml


@pytest.fixture()
def sample_project(tmp_path):
    """Create a temporary sample project for testing."""
    sample_dir = tmp_path / "sample_project"
    sample_dir.mkdir()

    # Create videos directory
    videos_dir = sample_dir / "videos"
    videos_dir.mkdir()

    # Create sample metadata files
    metadata1 = {
        "File": "test_video1.avi",
        "Species_name": "Test_species",
        "Date_start": "01/01/23",
        "Date_end": "01/01/23",
    }
    metadata2 = {
        "File": "test_video2.avi",
        "Species_name": "Test_species",
        "Date_start": "02/01/23",
        "Date_end": "02/01/23",
    }

    with open(videos_dir / "test_video1.metadata.yaml", "w") as f:
        yaml.dump(metadata1, f)
    with open(videos_dir / "test_video2.metadata.yaml", "w") as f:
        yaml.dump(metadata2, f)

    # Create metadata_fields.yaml
    metadata_fields = {
        "File": {"Type": "string", "LongName": "name of the video file"},
        "Species_name": {"Type": "string", "LongName": "Latin species name"},
        "Date_start": {
            "Type": "string",
            "LongName": "date in which the video recording started",
        },
        "Date_end": {
            "Type": "string",
            "LongName": "date in which the video recording terminated",
        },
    }

    with open(sample_dir / "metadata_fields.yaml", "w") as f:
        yaml.dump(metadata_fields, f)

    # Create project_config.yaml
    project_config = {
        "videos_dir_path": str(videos_dir),
        "metadata_fields_file_path": str(sample_dir / "metadata_fields.yaml"),
        "metadata_key_field_str": "File",
    }

    with open(sample_dir / "project_config.yaml", "w") as f:
        yaml.dump(project_config, f)

    return sample_dir
