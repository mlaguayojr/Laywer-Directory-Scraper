#Lawyer Class
from bs4 import BeautifulSoup
from re import compile
from decrypt import cfDecodeEmail

class Lawyer:

    def __init__(self, html_node):
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.office_phone = ""
        self.cell_phone = ""

        name = html_node.find("p", {"class": "profile-name"})
        name = name.text.split(' ')

        self.first_name = name[0]

        # Example of Suffixes
        if str(name[-1]).lower() in ["jr", "sr"]:
            self.last_name = name[-2:-1]
        else:
            self.last_name = name[-1]

        contact_node = html_node.find_all("a", {"href": compile(r'tel:*')})
        
        # Looks like Office is the first number
        if len(contact_node) > 0:
            self.office_phone = contact_node[0].text
            
            if len(contact_node) > 1:
                self.cell_phone = contact_node[1].text

        # Get Email
        email = html_node.find_all("a", {"class": "icon-email"})
        if len(email) == 1:
            self.email = email[0]["href"].replace("/cdn-cgi/l/email-protection#", "")

            # Email is encrypted - need to decrypt it as seen in (email-decode.min.js)
            # Luckily, someone's already done that work for us
            self.email = cfDecodeEmail(self.email)
        

    def __str__(self):
        return "Lawyer: %s %s | E: %s | O: %s | C: %s" % (self.first_name, self.last_name, self.email, self.office_phone, self.cell_phone)