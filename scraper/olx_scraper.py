from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time

from playwright.sync_api import sync_playwright


BASE_URL = "https://olx.com.lb/properties/apartments-villas-for-rent/"
BRAVE_PATH = "/usr/bin/brave-browser"


def fetch_page(page, url):

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(3000)

    return page.content()


def get_page_number(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    if not soup.title:
        return None

    title = soup.title.get_text(
        " ",
        strip=True
    )

    match = re.search(
        r"Page-(\d+)",
        title,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None


def parse_listings(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    unique_listings = {}

    links = soup.find_all(
        "a",
        href=re.compile(
            r"/ad/.*ID\d+\.html"
        )
    )

    for link in links:

        href = link.get("href")

        if not href:
            continue

        match = re.search(
            r"ID(\d+)\.html",
            href
        )

        if not match:
            continue

        external_id = match.group(1)

        url = urljoin(
            "https://olx.com.lb",
            href
        )

        if external_id not in unique_listings:

            unique_listings[external_id] = {
                "external_id": external_id,
                "url": url
            }

    return list(
        unique_listings.values()
    )


def scrape_olx():

    all_listings = []

    page_number = 1

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            executable_path=BRAVE_PATH,
            headless=True
        )

        page = browser.new_page()

        try:

            while True:

                if page_number == 1:
                    url = BASE_URL
                else:
                    url = (
                        f"{BASE_URL}"
                        f"?page={page_number}"
                    )

                print(
                    f"\nFetching page "
                    f"{page_number}..."
                )

                try:

                    html = fetch_page(
                        page,
                        url
                    )

                except Exception as e:

                    print(
                        f"\nError while fetching "
                        f"page {page_number}:"
                    )

                    print(e)

                    break

                actual_page = get_page_number(
                    html
                )

                # Page 1 does not contain
                # Page-1 in the title.
                if page_number == 1:

                    if actual_page is not None:

                        print(
                            f"\nUnexpected page "
                            f"number returned: "
                            f"{actual_page}"
                        )

                        break

                # Every page after page 1
                # must contain its own page number.
                else:

                    if actual_page != page_number:

                        print(
                            "\nReached the end "
                            "of OLX pagination."
                        )

                        print(
                            f"Requested page "
                            f"{page_number}, "
                            f"but OLX returned "
                            f"{actual_page if actual_page is not None else 'the main page'}."
                        )

                        break

                listings = parse_listings(
                    html
                )

                print(
                    f"Page {page_number}: "
                    f"{len(listings)} listings"
                )

                if not listings:

                    print(
                        "\nNo listings found. "
                        "Stopping."
                    )

                    break

                all_listings.extend(
                    listings
                )

                page_number += 1

                time.sleep(1)

        finally:

            browser.close()

    return all_listings


def remove_duplicates(listings):

    unique_listings = {}

    for listing in listings:

        external_id = listing[
            "external_id"
        ]

        if external_id not in unique_listings:

            unique_listings[
                external_id
            ] = listing

    return list(
        unique_listings.values()
    )


if __name__ == "__main__":

    listings = scrape_olx()

    unique_listings = remove_duplicates(
        listings
    )

    print("\n---")

    print(
        f"Total scraped listings: "
        f"{len(listings)}"
    )

    print(
        f"Unique listings: "
        f"{len(unique_listings)}"
    )

    print("\nUnique external IDs:")

    for listing in unique_listings:

        print(
            listing["external_id"]
        )