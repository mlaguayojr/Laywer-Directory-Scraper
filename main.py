#/bin/bash python3
from bs4 import BeautifulSoup
import requests

# Custom import
from lawyer import Lawyer

# Main URL for the website
url = "https://www.floridabar.org/directories/find-mbr/?"

# Build URL params
params = dict()
params["lName"] = ""
params["sdx"] = "N"
params["fName"] = ""
params["eligible"] = "Y"
params["deceased"] = "N"
params["firm"] = ""
params["locValue"] = "Florida"
params["locType"] = "S"
params["pracAreas"] = ""
params["lawSchool"] = ""
params["services"] = ""
params["langs"] = ""
params["certValue"] = ""
params["pageNumber"] = 1    # search results page number
params["pageSize"] = 50     # number of results to display on page

# build url based on params
for key in params.keys():
    url += "%s=%s&" % (key, params[key])

url = url.strip("&") # optional

try:

    req = requests.get(url)
    if req.status_code != 200:
        Exception("HTTP Error %s" % (req.status_code))

    soup = BeautifulSoup(req.content, "html.parser")
    
    contacts = soup.find_all("li", {"class": "profile-compact"})

    print("Request returned %s contacts" % (len(contacts)))

    lawyers = []

    for contact in contacts:
        lawyer_info = Lawyer(contact)
        print(lawyer_info)
        lawyers.append(lawyer_info)

except Exception as error:
    print("Error: %s" % (error) )
