import json
import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from olx_parser import parse_description
from olx_scraper import fetch_page, get_page_number, parse_listings
BRAVE_PATH = "/usr/bin/brave-browser"
BASE_URL = (
    "https://olx.com.lb/"
    "properties/apartments-villas-for-rent/"
)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "Chrome/150.0.0.0 Safari/537.36"
    )
}

def get_ad_data(url):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    for script in soup.find_all("script"):
        text = script.text.strip()
        if not text.startswith('{"props"'):
            continue
        data = json.loads(text)
        ad = (
            data["props"]
            ["pageProps"]
            ["initialState"]
            ["ad"]
            ["data"]
        )
        return ad, soup
    return None, soup

def extract_field(fields, attribute):
    for field in fields:
        if field.get("attribute") == attribute:
            return field.get("formattedValue")
    return None

def get_image_id_from_url(url):
    """Extract an OLX image ID from a supplied image URL."""
    match = re.search(
        r"/(?:thumbnails|image)/(\d+)(?:-|/)",
        url,
    )
    return match.group(1) if match else None

def extract_listing_photo_ids(soup, listing_id):
    """Extract photo IDs belonging to the current listing."""
    script = soup.find("script", id="__NEXT_DATA__")
    if not script or not script.string:
        print("WARNING: __NEXT_DATA__ not found.")
        return set()
    try:
        data = json.loads(script.string)
    except json.JSONDecodeError as error:
        print(
            "WARNING: Could not parse "
            f"__NEXT_DATA__: {error}"
        )
        return set()
    photo_ids = set()
    def walk(obj):
        if isinstance(obj, dict):
            if str(obj.get("externalID")) == str(listing_id):
                photos = obj.get("photos")
                if isinstance(photos, list):
                    for photo in photos:
                        if not isinstance(photo, dict):
                            continue
                        photo_id = photo.get("id")
                        if photo_id is not None:
                            photo_ids.add(str(photo_id))
                    if photo_ids:
                        return True
            for value in obj.values():
                if walk(value):
                    return True
        elif isinstance(obj, list):
            for item in obj:
                if walk(item):
                    return True
        return False
    walk(data)
    return photo_ids

def extract_images(soup, listing_id):
    """
    Extract image URLs supplied by OLX.
    WebP URLs are preferred when available.
    JPEG URLs are used as a fallback.
    """
    listing_photo_ids = extract_listing_photo_ids(
        soup,
        listing_id,
    )
    print(
        f"Listing photo IDs found: "
        f"{len(listing_photo_ids)}"
    )
    image_urls = {}
    for source in soup.find_all("source"):
        if source.get("type") != "image/webp":
            continue
        srcset = source.get("srcset")
        if not srcset:
            continue
        image_id = get_image_id_from_url(srcset)
        if image_id is None or image_id not in listing_photo_ids:
            continue
        image_urls.setdefault(
            image_id,
            {"webp": None, "jpeg": None},
        )
        image_urls[image_id]["webp"] = srcset
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        if "images-prod.olx-dubizzle.com" not in src:
            continue
        image_id = get_image_id_from_url(src)
        if image_id is None or image_id not in listing_photo_ids:
            continue
        image_urls.setdefault(
            image_id,
            {"webp": None, "jpeg": None},
        )
        image_urls[image_id]["jpeg"] = src
    selected_images = []
    for image_data in image_urls.values():
        if image_data["webp"]:
            selected_images.append(image_data["webp"])
        elif image_data["jpeg"]:
            selected_images.append(image_data["jpeg"])
    unique_images = []
    seen = set()
    for url in selected_images:
        if url in seen:
            continue
        seen.add(url)
        unique_images.append(url)
    return unique_images

def convert_price(value):
    if not value:
        return None
    try:
        return float(
            value.replace(",", "")
            .replace("USD", "")
            .strip()
        )
    except (ValueError, AttributeError):
        return None

def convert_size(value):
    if not value:
        return None
    try:
        return float(
            value.replace(",", "")
            .replace("SQM", "")
            .strip()
        )
    except (ValueError, AttributeError):
        return None
    
def convert_integer(value):
    if not value:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def extract_location(ad):
    location = ad.get("location", [])
    city = None
    area = None
    if len(location) >= 2:
        city = location[1].get("name")
    if len(location) >= 3:
        area = location[2].get("name")
    return city, area

def extract_seller_name(ad):
    contact = ad.get("contactInfo")
    if not isinstance(contact, dict):
        return None
    return contact.get("name")

def build_listing(ad, url, soup):
    description = ad.get("description")
    formatted_fields = ad.get("formattedExtraFields", [])
    listing = {
        "title": ad.get("title"),
        "description": description,
        "source": "OLX",
        "external_id": ad.get("externalID"),
        "url": url,
        "price": extract_field(formatted_fields, "price"),
        "currency": "USD",
        "city": None,
        "area": None,
        "property_type": extract_field(
            formatted_fields,
            "property_type",
        ),
        "bedrooms": extract_field(
            formatted_fields,
            "rooms",
        ),
        "bathrooms": extract_field(
            formatted_fields,
            "bathrooms",
        ),
        "size": extract_field(
            formatted_fields,
            "ft",
        ),
        "furnished": extract_field(
            formatted_fields,
            "furnished",
        ),
        "seller_name": None,
        "images": [],
    }
    listing["price"] = convert_price(listing["price"])
    listing["size"] = convert_size(listing["size"])
    listing["bedrooms"] = convert_integer(listing["bedrooms"])
    listing["bathrooms"] = convert_integer(listing["bathrooms"])
    listing["city"], listing["area"] = extract_location(ad)
    listing["seller_name"] = extract_seller_name(ad)
    listing["images"] = extract_images(
        soup,
        listing["external_id"],
    )
    parsed = parse_description(description)
    if listing["bedrooms"] is None:
        listing["bedrooms"] = parsed["bedrooms"]
    if listing["bathrooms"] is None:
        listing["bathrooms"] = parsed["bathrooms"]
    if listing["size"] is None:
        listing["size"] = parsed["size"]
    return listing

def scrape_details(url):
    ad, soup = get_ad_data(url)
    if not ad:
        return None
    formatted_fields = ad.get("formattedExtraFields", [])
    print("\n========== OLX FIELDS ==========")
    for field in formatted_fields:
        print(field)
    print("================================\n")
    return build_listing(ad, url, soup)

def get_page_url(page_number):
    if page_number == 1:
        return BASE_URL
    return f"{BASE_URL}?page={page_number}"

def get_listing_urls(limit=None):
    all_listings = []
    page_number = 1
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=BRAVE_PATH,
            headless=True,
        )
        page = browser.new_page()
        try:
            while True:
                url = get_page_url(page_number)
                print(
                    f"\nFetching OLX page "
                    f"{page_number}..."
                )
                html = fetch_page(page, url)
                actual_page = get_page_number(html)
                if page_number == 1:
                    if actual_page is not None:
                        print(
                            "\nUnexpected page number "
                            f"returned: {actual_page}"
                        )
                        break
                elif actual_page != page_number:
                    returned_page = (
                        actual_page
                        if actual_page is not None
                        else 1
                    )
                    print(
                        "\nReached the end of "
                        "OLX pagination."
                    )
                    print(
                        f"Requested page {page_number}, "
                        f"but OLX returned page "
                        f"{returned_page}."
                    )
                    break
                listings = parse_listings(html)
                print(
                    f"Page {page_number}: "
                    f"{len(listings)} listings"
                )
                if not listings:
                    print(
                        "\nNo listings found. Stopping."
                    )
                    break
                for listing in listings:
                    all_listings.append(listing)
                    if (
                        limit is not None
                        and len(all_listings) >= limit
                    ):
                        print(
                            f"\nReached test limit "
                            f"of {limit} listings."
                        )
                        return all_listings
                page_number += 1
                time.sleep(1)
        finally:
            browser.close()
    return all_listings

def remove_duplicates(listings):
    unique_listings = {}
    for listing in listings:
        external_id = listing["external_id"]
        if external_id not in unique_listings:
            unique_listings[external_id] = listing
    return list(unique_listings.values())

def print_usage():
    print("Usage:")
    print("python olx_detail_scraper.py")
    print("python olx_detail_scraper.py --limit 10")

def parse_limit_argument():
    if len(sys.argv) == 1:
        return None
    if len(sys.argv) != 3 or sys.argv[1] != "--limit":
        print_usage()
        sys.exit(1)
    try:
        limit = int(sys.argv[2])
    except ValueError:
        print("Limit must be a number.")
        sys.exit(1)
    if limit <= 0:
        print("Limit must be greater than 0.")
        sys.exit(1)
    return limit

def scrape_all_details(listings):
    detailed_listings = []
    total = len(listings)
    for index, listing in enumerate(listings, start=1):
        url = listing["url"]
        external_id = listing["external_id"]
        print(
            f"\n[{index}/{total}] Scraping:"
        )
        print(url)
        try:
            detailed_listing = scrape_details(url)
            if detailed_listing:
                detailed_listings.append(detailed_listing)
                print(
                    f"Successfully scraped "
                    f"{external_id}"
                )
            else:
                print(
                    f"Failed to scrape "
                    f"{external_id}"
                )
        except requests.exceptions.RequestException as error:
            print(
                f"Request failed for "
                f"{external_id}:"
            )
            print(error)
        except (
            KeyError,
            TypeError,
            json.JSONDecodeError,
        ) as error:
            print(
                f"Failed to parse "
                f"{external_id}:"
            )
            print(error)
    return detailed_listings

def print_results(detailed_listings):
    print("\n---")
    print(
        f"Successfully scraped details: "
        f"{len(detailed_listings)}"
    )
    for listing in detailed_listings:
        print("\n--- LISTING ---")
        for key, value in listing.items():
            if key == "images":
                print(
                    f"{key}: "
                    f"{len(value)} images"
                )
            else:
                print(f"{key}: {value}")

if __name__ == "__main__":
    limit = parse_limit_argument()
    listings = get_listing_urls(limit=limit)
    unique_listings = remove_duplicates(listings)
    print("\n---")
    print(
        f"Total scraped listing URLs: "
        f"{len(listings)}"
    )
    print(
        f"Unique listing URLs: "
        f"{len(unique_listings)}"
    )
    print("\nStarting detail scraping...")
    detailed_listings = scrape_all_details(
        unique_listings
    )
    print_results(detailed_listings)