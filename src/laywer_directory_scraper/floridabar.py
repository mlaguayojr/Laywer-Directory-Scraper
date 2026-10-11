from .location import Location
from .lawyer import Lawyer
from bs4 import BeautifulSoup
import requests
import re

class FloridaBar:

    def __init__(self):
        self.search_url: str = "https://www.floridabar.org/directories/find-mbr/?"

    def __toYesOrNo(self, value: bool) -> str:
        return "Y" if value else "N"

    def search(self,
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
        pageNumber: int = 1,
        pageSize: int = 10):
        """
        Perform a search with provided criteria.
        NOTE: if bar_number is provided, other fields are ignored.
        """
        
        query_params = {}

        try:

            if bar_number is not None:

                if "*" in bar_number:
                    raise Exception("Wildcards (\"*\") are not allowed.")

                barNum = bar_number.lstrip('0')

                if len(barNum) == 0:
                    raise Exception("Provided bar_number does not contain valid data.")
                
                query_params["barNum"] = int(barNum)

            else:
                print("searching with provided values...")

                if not last_name.strip():
                    query_params['lName'] = last_name
                
                if not first_name.strip():
                    query_params['fName'] = first_name

                if not law_firm.strip():
                    query_params['firm'] = law_firm

                query_params['locType'] = location_type.value
                query_params['locValue'] = location_value

                if pro_bono:
                    query_params['services'] = "PBS"

                query_params['sdx'] = self.__toYesOrNo(sounds_like)
                query_params['eligible'] = self.__toYesOrNo(eligible)
                query_params['deceased'] = self.__toYesOrNo(deceased)

                query_params['pageNumber'] = pageNumber
                query_params['pageSize'] = pageSize

                if not pageSize in [10, 25, 50]:
                    raise Exception("pageSize must be either 10, 25, or 50")

                query_params['langs'] = 'ENGL'

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            request = requests.get(
                self.search_url,
                params=query_params,
                headers=headers)

            if request.status_code == 200:
                if "Too many results. Please enter additional search parameters and try again." in str(request.content):
                    raise Exception("Too many results. Please enter additional search parameters and try again.")

            self.soup = BeautifulSoup(request.content, "html.parser")
            
            # find search results
            search_count_text = self.soup.find(
                name="p",
                attrs={"class": "result-message"})
            
            search_count_text = re.sub(r'\s+', ' ', str(search_count_text.contents[0])).strip()
            
            print(search_count_text)

            max_page = self.soup.find("ul", "member-pagination paging-controls").findChildren("li")[-2].get_text(strip=True)
            self.max_pages: int = int(max_page.replace(",", ""))

            print(f"max # of pages: {self.max_pages}")

            self.lawyers = []

            profiles = self.soup.find_all(
                name="li",
                attrs={"class": "profile-compact"})

            for profile in profiles:
                lawyer_info = Lawyer(profile)
                print(lawyer_info)
                self.lawyers.append(lawyer_info)

        except Exception as e:
            pass