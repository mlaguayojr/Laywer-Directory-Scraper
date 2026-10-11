#Lawyer Class
from bs4 import BeautifulSoup
from re import compile
from .decrypt import cfDecodeEmail

class Lawyer:

    def __init__(self, html_node):
        self.name: str = ""
        self.bar_number: str = ""
        self.address: str = ""
        self.office_phone: str = ""
        self.cell_phone: str = ""
        self.email :str = ""
        

        name = html_node.find(name="p", attrs={"class": "profile-name"})
        self.name = name.get_text().strip()
        
        bar_number = html_node.find(name="p", attrs={"class": "profile-bar-number"})
        self.bar_number = int(bar_number.get_text().strip().replace("Bar #", ""))

        contact_info = html_node.find(name="div", attrs={"class": "profile-contact"})
        
        self.address = contact_info.find("p").get_text(separator=", ", strip=True)

        contact_number = html_node.find_all("a", {"href": compile(r'tel:*')})
        
        # Looks like Office is the first number
        if len(contact_number) > 0:
            self.office_phone = contact_number[0].text
            
            # Cell Phone tends to be the second number
            if len(contact_number) > 1:
                self.cell_phone = contact_number[1].text

        # Get Email
        email = html_node.find_all("a", {"class": "icon-email"})
        if len(email) == 1:
            self.email = email[0]["href"].replace("/cdn-cgi/l/email-protection#", "")

            # Email is encrypted - need to decrypt it as seen in (email-decode.min.js)
            self.email = cfDecodeEmail(self.email)

    def __str__(self) -> str:
        return f"Bar#: {self.bar_number} | Name: {self.name} | Address: {self.address} | Office#: {self.office_phone} | Cell#: {self.cell_phone} | Email: {self.email}"