import logging
import re

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .lawyer import Lawyer
from .location import Location

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS = 10


class FloridaBarSearchError(Exception):
    """Raised when a search against the Florida Bar directory cannot be completed."""


class FloridaBar:
    def __init__(self):
        self.search_url: str = "https://www.floridabar.org/directories/find-mbr/?"
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.lawyers: list[Lawyer] = []
        self.max_pages: int = 0

    def __to_yes_or_no(self, value: bool) -> str:
        return "Y" if value else "N"

    def _build_query_params(
        self,
        bar_number: str | None = None,
        first_name: str = "",
        last_name: str = "",
        law_firm: str = "",
        location_type: Location = Location.State,
        location_value: str = "Florida",
        pro_bono: bool = False,
        sounds_like: bool = False,
        eligible: bool = False,
        deceased: bool = False,
        page_number: int = 1,
        page_size: int = 10,
    ) -> dict:
        """Build the query-string parameters for a directory search."""

        query_params = {}

        if bar_number is not None:
            if "*" in bar_number:
                raise FloridaBarSearchError('Wildcards ("*") are not allowed.')

            bar_num = bar_number.lstrip("0")

            if len(bar_num) == 0:
                raise FloridaBarSearchError("Provided bar_number does not contain valid data.")

            query_params["barNum"] = int(bar_num)

            return query_params

        logger.debug("searching with provided values...")

        if last_name.strip():
            query_params["lName"] = last_name

        if first_name.strip():
            query_params["fName"] = first_name

        if law_firm.strip():
            query_params["firm"] = law_firm

        query_params["locType"] = location_type.value
        query_params["locValue"] = location_value

        if pro_bono:
            query_params["services"] = "PBS"

        query_params["sdx"] = self.__to_yes_or_no(sounds_like)
        query_params["eligible"] = self.__to_yes_or_no(eligible)
        query_params["deceased"] = self.__to_yes_or_no(deceased)

        if page_size not in [10, 25, 50]:
            raise FloridaBarSearchError("page_size must be either 10, 25, or 50")

        query_params["pageNumber"] = page_number
        query_params["pageSize"] = page_size

        query_params["langs"] = "ENGL"

        return query_params

    def search(
        self,
        bar_number: str | None = None,
        first_name: str = "",
        last_name: str = "",
        law_firm: str = "",
        location_type: Location = Location.State,
        location_value: str = "Florida",
        pro_bono: bool = False,
        sounds_like: bool = False,
        eligible: bool = False,
        deceased: bool = False,
        page_number: int = 1,
        page_size: int = 10,
    ):
        """
        Perform a search with provided criteria.
        NOTE: if bar_number is provided, other fields are ignored.
        """

        query_params = self._build_query_params(
            bar_number=bar_number,
            first_name=first_name,
            last_name=last_name,
            law_firm=law_firm,
            location_type=location_type,
            location_value=location_value,
            pro_bono=pro_bono,
            sounds_like=sounds_like,
            eligible=eligible,
            deceased=deceased,
            page_number=page_number,
            page_size=page_size,
        )

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        try:
            request = self.session.get(
                self.search_url,
                params=query_params,
                headers=headers,
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )
            request.raise_for_status()

        except requests.RequestException as e:
            logger.exception("Request to Florida Bar directory failed")
            raise FloridaBarSearchError("Failed to reach the Florida Bar directory") from e

        too_many_results_message = (
            "Too many results. Please enter additional search parameters and try again."
        )

        if too_many_results_message in str(request.content):
            raise FloridaBarSearchError(too_many_results_message)

        self.soup = BeautifulSoup(request.content, "html.parser")

        # find search results
        search_count_text = self.soup.find(name="p", attrs={"class": "result-message"})

        search_count_text = re.sub(r"\s+", " ", str(search_count_text.contents[0])).strip()

        logger.info(search_count_text)

        pagination = self.soup.find("ul", "member-pagination paging-controls")
        max_page = pagination.findChildren("li")[-2].get_text(strip=True)
        self.max_pages = int(max_page.replace(",", ""))

        logger.debug("max # of pages: %s", self.max_pages)

        self.lawyers = []

        profiles = self.soup.find_all(name="li", attrs={"class": "profile-compact"})

        for profile in profiles:
            lawyer_info = Lawyer(profile)
            logger.debug("%s", lawyer_info)
            self.lawyers.append(lawyer_info)
