from urllib.parse import urljoin
import re
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
BASE_URL = "https://olx.com.lb/properties/apartments-villas-for-rent/"
BASE_DOMAIN = "https://olx.com.lb"
BRAVE_PATH = "/usr/bin/brave-browser"

def fetch_page(page, url):
    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000,
    )
    page.wait_for_timeout(3000)
    return page.content()

def get_page_number(html):
    soup = BeautifulSoup(html, "html.parser")
    if not soup.title:
        return None
    title = soup.title.get_text(" ", strip=True)
    match = re.search(r"Page-(\d+)", title, re.IGNORECASE)
    return int(match.group(1)) if match else None

def parse_listings(html):
    soup = BeautifulSoup(html, "html.parser")
    unique_listings = {}
    links = soup.find_all(
        "a",
        href=re.compile(r"/ad/.*ID\d+\.html"),
    )
    for link in links:
        href = link.get("href")
        if not href:
            continue
        match = re.search(r"ID(\d+)\.html", href)
        if not match:
            continue
        external_id = match.group(1)
        unique_listings[external_id] = {
            "external_id": external_id,
            "url": urljoin(BASE_DOMAIN, href),
        }
    return list(unique_listings.values())

def get_page_url(page_number):
    if page_number == 1:
        return BASE_URL
    return f"{BASE_URL}?page={page_number}"

def is_expected_page(html, page_number):
    actual_page = get_page_number(html)
    if page_number == 1:
        return actual_page is None
    return actual_page == page_number

def scrape_olx():
    all_listings = []
    page_number = 1
    scrape_complete = False
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=BRAVE_PATH,
            headless=True,
        )
        page = browser.new_page()
        try:
            while True:
                url = get_page_url(page_number)
                print(f"\nFetching page {page_number}...")
                try:
                    html = fetch_page(page, url)
                except Exception as error:
                    print(
                        f"\nError while fetching page "
                        f"{page_number}:"
                    )
                    print(error)
                    print(
                        "\nOLX scrape is incomplete. "
                        "Existing listings will not be deleted."
                    )
                    break
                actual_page = get_page_number(html)
                if not is_expected_page(html, page_number):
                    if page_number == 1:
                        print(
                            f"\nUnexpected page number returned: "
                            f"{actual_page}"
                        )
                    else:
                        returned_page = (
                            actual_page
                            if actual_page is not None
                            else "the main page"
                        )
                        print(
                            "\nReached the end of OLX pagination."
                        )
                        print(
                            f"Requested page {page_number}, "
                            f"but OLX returned {returned_page}."
                        )
                        scrape_complete = True
                    if page_number == 1:
                        print(
                            "\nOLX scrape is incomplete. "
                            "Existing listings will not be deleted."
                        )
                    break
                listings = parse_listings(html)
                print(
                    f"Page {page_number}: "
                    f"{len(listings)} listings"
                )
                if not listings:
                    print("\nNo listings found. Stopping.")
                    scrape_complete = True
                    break
                all_listings.extend(listings)
                page_number += 1
                time.sleep(1)
        finally:
            browser.close()
    return all_listings, scrape_complete

def remove_duplicates(listings):
    unique_listings = {}
    for listing in listings:
        external_id = listing["external_id"]
        if external_id not in unique_listings:
            unique_listings[external_id] = listing
    return list(unique_listings.values())

if __name__ == "__main__":
    listings, scrape_complete = scrape_olx()
    unique_listings = remove_duplicates(listings)
    print("\n---")
    print(f"Total scraped listings: {len(listings)}")
    print(f"Unique listings: {len(unique_listings)}")
    print(f"Scrape complete: {scrape_complete}")
    print("\nUnique external IDs:")
    for listing in unique_listings:
        print(listing["external_id"])