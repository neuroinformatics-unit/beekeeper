import pytest
import selenium
import yaml
from dash.testing.composite import DashComposite

from beekeeper.app import app


@pytest.fixture
def sample_project_with_key_field(sample_project, request):
    """Modify the sample project to use a specific key metadata field.

    Parameters
    ----------
    sample_project : Path
        The base sample project fixture
    request : pytest.FixtureRequest
        Pytest request object to access test parameters

    Returns
    -------
    Path
        Path to the sample project with modified config
    """
    key_field = request.param

    # Read existing project config and only modify the key field
    with open(sample_project / "project_config.yaml", "r") as f:
        project_config = yaml.safe_load(f)

    # Modify only the metadata_key_field_str
    project_config["metadata_key_field_str"] = key_field

    # Write back the modified config
    with open(sample_project / "project_config.yaml", "w") as f:
        yaml.dump(project_config, f)

    return sample_project


@pytest.mark.parametrize(
    "sample_project_with_key_field", ["File", "Date_start"], indirect=True
)
def test_key_metadata_field_first_column(
    dash_duo: DashComposite,
    sample_project_with_key_field,
    timeout: float,
    request,
) -> None:
    """Test that the key metadata field appears as the first column in the table.

    This test verifies that regardless of what field is specified as the key field,
    it always appears as the first column in the metadata table.

    Parameters
    ----------
    dash_duo : DashComposite
        Default fixture for Dash Python integration tests.
    sample_project_with_key_field : Path
        Fixture providing a sample project with modified key field
    timeout : float
        maximum time to wait in seconds for a component
    request : pytest.FixtureRequest
        Pytest request object to access test parameters
    """
    key_field = request.node.callspec.params["sample_project_with_key_field"]

    # Start server
    dash_duo.start_server(app)

    # Navigate to Home page
    dash_duo.find_element("#sidebar #link-Home").click()
    dash_duo.wait_for_text_to_equal("h1", "Home", timeout=timeout)

    # Upload the project config file
    upload_element = dash_duo.find_element("#upload-config-file input[type='file']")
    config_path = str(sample_project_with_key_field / "project_config.yaml")
    upload_element.send_keys(config_path)

    # Wait for config to be processed
    try:
        dash_duo.wait_for_text_to_equal(
            "#alert div", "Configuration file uploaded successfully!", timeout=timeout
        )
    except selenium.common.exceptions.TimeoutException:
        pytest.fail("Config upload alert not shown")

    # Navigate to metadata page
    dash_duo.find_element("#sidebar #link-01-metadata").click()
    dash_duo.wait_for_text_to_equal("h1", "Metadata", timeout=timeout)

    # Wait for metadata table to load
    try:
        dash_duo.wait_for_element("#metadata-table", timeout=timeout)
    except selenium.common.exceptions.TimeoutException:
        pytest.fail("Metadata table not generated")

    # Get the table headers to verify column ordering
    table_headers = dash_duo.find_elements("#metadata-table thead th")

    # Verify that the key field is the first column
    assert len(table_headers) >= 4, "Table should have at least 4 columns"
    first_column_text = table_headers[0].text.strip()
    assert (
        first_column_text == key_field
    ), f"First column should be '{key_field}' but was '{first_column_text}'"

    # Verify other expected columns are present
    all_headers = [header.text.strip() for header in table_headers]
    expected_columns = ["File", "Species_name", "Date_start", "Date_end"]
    for col in expected_columns:
        assert (
            col in all_headers
        ), f"Column '{col}' not found in table headers: {all_headers}"

    # Check for console errors
    logs = dash_duo.get_logs()
    assert logs == [], f"There are {len(logs)} errors in the browser console!"
