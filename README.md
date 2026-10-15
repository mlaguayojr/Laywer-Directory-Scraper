# Laywer-Directory-Scraper

A small Python scraper for the [Florida Bar member directory](https://www.floridabar.org/directories/find-mbr/).

While browsing /r/programming, I found this thread:
https://www.reddit.com/r/programming/comments/inhelx/trying_to_scrape_a_website_but_i_am_a_idiot_any/

I thought this would be a good chance to brush-up on my Python (since I've been using C#/.NET since 2022).

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync --group dev
```

## Usage

As a library:

```python
from laywer_directory_scraper.floridabar import FloridaBar

client = FloridaBar()
client.search(last_name="Doe")

for lawyer in client.lawyers:
    print(lawyer)
```

As a CLI:

```bash
uv run laywer-directory-scraper --last-name Doe --output results.csv
```

Run `uv run laywer-directory-scraper --help` for all available filters (`--first-name`, `--firm`, `--bar-number`, `-v/--verbose` for debug logging).

## Development

```bash
uv run pytest          # run tests
uv run ruff check .    # lint
uv run ruff format .   # format
```

## A note on scope
This project scrapes a public directory page and includes a helper to decode Cloudflare's email-obfuscation markup so that already-public contact emails are human-readable, rather than to bypass any access control.

It does not attempt to defeat CAPTCHAs, authentication, or rate limiting, and does not check `robots.txt` automatically — if you adapt this for other sites or heavier use, review that site's terms of service and `robots.txt` first, and keep request volume reasonable.

This does basic search functions available to the online form and does not include the additional search options available. 