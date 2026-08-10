import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time


BASE_URL = "https://olx.com.lb/properties/apartments-villas-for-rent/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/150.0.0.0 Safari/537.36"
    )
}


def fetch_page(url, timeout=30):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=timeout
    )

    response.raise_for_status()

    return response.text


def get_page_number(html):
    soup = BeautifulSoup(html, "html.parser")

    if not soup.title:
        return None

    title = soup.title.get_text(" ", strip=True)

    match = re.search(
        r"Page-(\d+)",
        title,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None


def parse_listings(html):
    soup = BeautifulSoup(html, "html.parser")

    unique_listings = {}

    links = soup.find_all(
        "a",
        href=re.compile(r"/ad/.*ID\d+\.html")
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

    return list(unique_listings.values())


def scrape_olx():

    all_listings = []

    page = 1

    while True:

        if page == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}?page={page}"

        try:
            html = fetch_page(url)

        except requests.exceptions.RequestException as e:

            print(f"\nError while fetching page {page}:")
            print(e)

            break

        actual_page = get_page_number(html)

        # Page 1 does not contain Page-1 in the title
        if page == 1:

            if actual_page is not None:

                print(
                    f"\nUnexpected page number returned: "
                    f"{actual_page}"
                )

                break

        # Every page after page 1 must contain its
        # own page number in the title
        else:

            if actual_page != page:

                print("\nReached the end of OLX pagination.")

                print(
                    f"Requested page {page}, "
                    f"but OLX returned "
                    f"{actual_page if actual_page is not None else 'the main page'}."
                )

                break

        listings = parse_listings(html)

        print(
            f"\nPage {page}: "
            f"{len(listings)} listings"
        )

        # If a valid page contains no listings,
        # stop the scraper.
        if not listings:

            print("\nNo listings found. Stopping.")

            break

        all_listings.extend(listings)

        page += 1

        time.sleep(1)

    return all_listings


def remove_duplicates(listings):

    unique_listings = {}

    for listing in listings:

        external_id = listing["external_id"]

        if external_id not in unique_listings:

            unique_listings[external_id] = listing

    return list(unique_listings.values())


if __name__ == "__main__":

    listings = scrape_olx()

    unique_listings = remove_duplicates(listings)

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