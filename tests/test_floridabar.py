import pytest

from laywer_directory_scraper.floridabar import FloridaBar, FloridaBarSearchError
from laywer_directory_scraper.location import Location


@pytest.fixture
def client():
    return FloridaBar()


def test_last_name_filter_is_included_when_provided(client):
    params = client._build_query_params(last_name="Doe")
    assert params["lName"] == "Doe"


def test_first_name_filter_is_included_when_provided(client):
    params = client._build_query_params(first_name="Jane")
    assert params["fName"] == "Jane"


def test_law_firm_filter_is_included_when_provided(client):
    params = client._build_query_params(law_firm="Doe & Associates")
    assert params["firm"] == "Doe & Associates"


def test_blank_filters_are_omitted(client):
    params = client._build_query_params(last_name="  ", first_name="", law_firm="")
    assert "lName" not in params
    assert "fName" not in params
    assert "firm" not in params


def test_bar_number_search_ignores_other_filters(client):
    params = client._build_query_params(bar_number="012345", last_name="Doe")
    assert params == {"barNum": 12345}


def test_bar_number_with_wildcard_raises(client):
    with pytest.raises(FloridaBarSearchError):
        client._build_query_params(bar_number="123*")


def test_bar_number_all_zeros_raises(client):
    with pytest.raises(FloridaBarSearchError):
        client._build_query_params(bar_number="000")


def test_invalid_page_size_raises(client):
    with pytest.raises(FloridaBarSearchError):
        client._build_query_params(last_name="Doe", page_size=15)


def test_location_and_paging_defaults(client):
    params = client._build_query_params(last_name="Doe")
    assert params["locType"] == Location.State.value
    assert params["locValue"] == "Florida"
    assert params["pageNumber"] == 1
    assert params["pageSize"] == 10
