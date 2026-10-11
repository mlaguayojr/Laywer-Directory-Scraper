from bs4 import BeautifulSoup

from laywer_directory_scraper.lawyer import Lawyer

PROFILE_HTML = """
<li class="profile-compact">
    <p class="profile-name">Jane Doe</p>
    <p class="profile-bar-number">Bar #123456</p>
    <div class="profile-contact">
        <p>123 Main St, Tallahassee, FL 32301</p>
        <a href="tel:8505551234">(850) 555-1234</a>
        <a href="tel:8505555678">(850) 555-5678</a>
        <a class="icon-email"
           href="/cdn-cgi/l/email-protection#1a707e757f5a7f627b776a767f34797577">Email</a>
    </div>
</li>
"""


def _parse_profile(html: str) -> Lawyer:
    soup = BeautifulSoup(html, "html.parser")
    node = soup.find("li", {"class": "profile-compact"})
    return Lawyer(node)


def test_parses_name_and_bar_number():
    lawyer = _parse_profile(PROFILE_HTML)
    assert lawyer.name == "Jane Doe"
    assert lawyer.bar_number == 123456


def test_parses_address():
    lawyer = _parse_profile(PROFILE_HTML)
    assert lawyer.address == "123 Main St, Tallahassee, FL 32301"


def test_parses_office_and_cell_phone():
    lawyer = _parse_profile(PROFILE_HTML)
    assert lawyer.office_phone == "(850) 555-1234"
    assert lawyer.cell_phone == "(850) 555-5678"


def test_decodes_email():
    lawyer = _parse_profile(PROFILE_HTML)
    assert lawyer.email == "jdoe@example.com"


def test_missing_phone_numbers_default_to_empty():
    html_without_phones = """
    <li class="profile-compact">
        <p class="profile-name">John Smith</p>
        <p class="profile-bar-number">Bar #654321</p>
        <div class="profile-contact">
            <p>456 Oak Ave, Miami, FL 33101</p>
        </div>
    </li>
    """
    lawyer = _parse_profile(html_without_phones)
    assert lawyer.office_phone == ""
    assert lawyer.cell_phone == ""
    assert lawyer.email == ""


def test_to_dict_contains_all_fields():
    lawyer = _parse_profile(PROFILE_HTML)
    assert lawyer.to_dict() == {
        "name": "Jane Doe",
        "bar_number": 123456,
        "address": "123 Main St, Tallahassee, FL 32301",
        "office_phone": "(850) 555-1234",
        "cell_phone": "(850) 555-5678",
        "email": "jdoe@example.com",
    }
