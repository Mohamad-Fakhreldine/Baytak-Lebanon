import requests
import json
import sys
import time
import re

from bs4 import BeautifulSoup

from olx_parser import parse_description
from olx_scraper import fetch_page, get_page_number, parse_listings


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "Chrome/150.0.0.0 Safari/537.36"
    )
}


BASE_URL = (
    "https://olx.com.lb/"
    "properties/apartments-villas-for-rent/"
)


# ---------------------------------------------------------
# GET AD DATA
# ---------------------------------------------------------

def get_ad_data(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "lxml"
    )

    for script in soup.find_all("script"):

        text = script.text.strip()

        if text.startswith('{"props"'):

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


# ---------------------------------------------------------
# EXTRACT FIELD
# ---------------------------------------------------------

def extract_field(fields, attribute):

    for field in fields:

        if field.get("attribute") == attribute:

            return field.get(
                "formattedValue"
            )

    return None


# ---------------------------------------------------------
# GET IMAGE ID FROM URL
# ---------------------------------------------------------

def get_image_id_from_url(url):
    """
    Extract the OLX image ID from a dynamically supplied URL.

    Examples:

        /thumbnails/17426144-400x300.jpeg
        /thumbnails/17426144-400x600.jpeg
        /image/17426144/....

    We only use this to identify which image belongs
    to the listing.

    We do NOT construct or modify image URLs.
    """

    match = re.search(
        r"/(?:thumbnails|image)/(\d+)(?:-|/)",
        url
    )

    if match:
        return match.group(1)

    return None


# ---------------------------------------------------------
# EXTRACT LISTING PHOTO IDS
# ---------------------------------------------------------

def extract_listing_photo_ids(soup, listing_id):
    """
    Extract the photo IDs belonging to THIS listing from
    OLX's __NEXT_DATA__.

    We do not construct any image URLs here.
    """

    script = soup.find(
        "script",
        id="__NEXT_DATA__"
    )

    if not script or not script.string:

        print(
            "WARNING: __NEXT_DATA__ not found."
        )

        return set()

    try:

        data = json.loads(
            script.string
        )

    except json.JSONDecodeError as e:

        print(
            f"WARNING: Could not parse "
            f"__NEXT_DATA__: {e}"
        )

        return set()

    photo_ids = set()

    def walk(obj):

        if isinstance(obj, dict):

            if (
                str(obj.get("externalID"))
                == str(listing_id)
            ):

                photos = obj.get("photos")

                if isinstance(photos, list):

                    for photo in photos:

                        if not isinstance(
                            photo,
                            dict
                        ):
                            continue

                        photo_id = photo.get("id")

                        if photo_id is not None:

                            photo_ids.add(
                                str(photo_id)
                            )

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


# ---------------------------------------------------------
# EXTRACT IMAGES
# ---------------------------------------------------------

def extract_images(soup, listing_id):
    """
    Extract image URLs exactly as supplied by OLX.

    OLX supplies the same displayed image in multiple formats:
        - WebP <source>
        - JPEG <img>

    We keep only ONE URL per image ID, preferring WebP.

    We do NOT construct or modify image URLs.
    """

    # -----------------------------------------------------
    # Get photo IDs belonging to this listing
    # -----------------------------------------------------

    listing_photo_ids = extract_listing_photo_ids(
        soup,
        listing_id
    )

    print(
        f"Listing photo IDs found: "
        f"{len(listing_photo_ids)}"
    )

    # -----------------------------------------------------
    # Collect dynamically supplied image URLs
    # -----------------------------------------------------

    # image_id -> {
    #     "webp": URL or None,
    #     "jpeg": URL or None
    # }

    image_urls = {}

    # -----------------------------------------------------
    # First: WebP <source> URLs
    # -----------------------------------------------------

    for source in soup.find_all("source"):

        source_type = source.get("type")
        srcset = source.get("srcset")

        if source_type != "image/webp":
            continue

        if not srcset:
            continue

        image_id = get_image_id_from_url(
            srcset
        )

        if image_id is None:
            continue

        if image_id not in listing_photo_ids:
            continue

        if image_id not in image_urls:

            image_urls[image_id] = {
                "webp": None,
                "jpeg": None
            }

        image_urls[image_id]["webp"] = srcset

    # -----------------------------------------------------
    # Second: regular <img> URLs
    # -----------------------------------------------------

    for img in soup.find_all("img"):

        src = img.get("src")

        if not src:
            continue

        if (
            "images-prod.olx-dubizzle.com"
            not in src
        ):
            continue

        image_id = get_image_id_from_url(
            src
        )

        if image_id is None:
            continue

        if image_id not in listing_photo_ids:
            continue

        if image_id not in image_urls:

            image_urls[image_id] = {
                "webp": None,
                "jpeg": None
            }

        image_urls[image_id]["jpeg"] = src

    # -----------------------------------------------------
    # Choose ONE URL per image
    #
    # Prefer WebP because it worked in testing.
    # Fall back to JPEG if no WebP was supplied.
    # -----------------------------------------------------

    selected_images = []

    for image_id in image_urls:

        webp_url = image_urls[
            image_id
        ]["webp"]

        jpeg_url = image_urls[
            image_id
        ]["jpeg"]

        if webp_url:

            selected_images.append(
                webp_url
            )

        elif jpeg_url:

            selected_images.append(
                jpeg_url
            )

    # -----------------------------------------------------
    # Remove duplicates while preserving order
    # -----------------------------------------------------

    unique_images = []

    seen = set()

    for url in selected_images:

        if url in seen:
            continue

        seen.add(url)

        unique_images.append(url)

    return unique_images


# ---------------------------------------------------------
# SCRAPE ONE LISTING
# ---------------------------------------------------------

def scrape_details(url):

    ad, soup = get_ad_data(url)

    if not ad:
        return None

    description = ad.get(
        "description"
    )

    formatted_fields = ad.get(
        "formattedExtraFields",
        []
    )

    print("\n========== OLX FIELDS ==========")

    for field in formatted_fields:
        print(field)

    print("================================\n")

    location = ad.get(
        "location",
        []
    )

    location = ad.get(
        "location",
        []
    )

    listing = {

        "title": ad.get("title"),

        "description": description,

        "source": "OLX",

        "external_id": ad.get(
            "externalID"
        ),

        "url": url,

        "price": None,

        "currency": "USD",

        "city": None,

        "area": None,

        "address": None,

        "property_type": None,

        "bedrooms": None,

        "bathrooms": None,

        "size": None,

        "seller_name": None,

        "images": []

    }

    # -----------------------------------------------------
    # Structured fields
    # -----------------------------------------------------

    listing["price"] = extract_field(
        formatted_fields,
        "price"
    )

    listing["size"] = extract_field(
        formatted_fields,
        "ft"
    )

    listing["property_type"] = extract_field(
        formatted_fields,
        "type"
    )

    # -----------------------------------------------------
    # Convert price
    # -----------------------------------------------------

    if listing["price"]:

        try:

            listing["price"] = float(
                listing["price"]
                .replace(",", "")
                .replace("USD", "")
                .strip()
            )

        except (
            ValueError,
            AttributeError
        ):

            listing["price"] = None

    # -----------------------------------------------------
    # Convert size
    # -----------------------------------------------------

    if listing["size"]:

        try:

            listing["size"] = float(
                listing["size"]
                .replace(",", "")
                .replace("SQM", "")
                .strip()
            )

        except (
            ValueError,
            AttributeError
        ):

            listing["size"] = None

    # -----------------------------------------------------
    # Location
    # -----------------------------------------------------

    if len(location) >= 2:

        listing["city"] = (
            location[1]
            .get("name")
        )

    if len(location) >= 3:

        listing["area"] = (
            location[2]
            .get("name")
        )

    # -----------------------------------------------------
    # Seller
    # -----------------------------------------------------

    contact = ad.get(
        "contactInfo"
    )

    if isinstance(contact, dict):

        listing["seller_name"] = (
            contact.get("name")
        )

    # -----------------------------------------------------
    # Images
    # -----------------------------------------------------

    listing["images"] = extract_images(
        soup,
        listing["external_id"]
    )

    # -----------------------------------------------------
    # Parser fallback
    # -----------------------------------------------------

    parsed = parse_description(
        description
    )

    if listing["bedrooms"] is None:

        listing["bedrooms"] = (
            parsed["bedrooms"]
        )

    if listing["bathrooms"] is None:

        listing["bathrooms"] = (
            parsed["bathrooms"]
        )

    if listing["size"] is None:

        listing["size"] = (
            parsed["size"]
        )

    return listing


# ---------------------------------------------------------
# GET LISTING URLS WITH LIMIT
# ---------------------------------------------------------

def get_listing_urls(limit=None):

    all_listings = []

    page = 1

    while True:

        if page == 1:

            url = BASE_URL

        else:

            url = (
                f"{BASE_URL}?page={page}"
            )

        try:

            html = fetch_page(url)

        except requests.exceptions.RequestException as e:

            print(
                f"\nError while fetching page {page}:"
            )

            print(e)

            break

        actual_page = get_page_number(
            html
        )

        # -------------------------------------------------
        # Page 1
        # -------------------------------------------------

        if page == 1:

            if actual_page is not None:

                print(
                    f"\nUnexpected page number returned: "
                    f"{actual_page}"
                )

                break

        # -------------------------------------------------
        # Pages after page 1
        # -------------------------------------------------

        else:

            if actual_page != page:

                print(
                    "\nReached the end of OLX pagination."
                )

                returned_page = (
                    actual_page
                    if actual_page is not None
                    else 1
                )

                print(
                    f"Requested page {page}, "
                    f"but OLX returned page "
                    f"{returned_page}."
                )

                break

        listings = parse_listings(
            html
        )

        print(
            f"Page {page}: "
            f"{len(listings)} listings"
        )

        if not listings:

            print(
                "\nNo listings found. Stopping."
            )

            break

        # -------------------------------------------------
        # Add listings
        # -------------------------------------------------

        for listing in listings:

            all_listings.append(
                listing
            )

            # Stop immediately once the
            # requested test limit is reached.

            if (
                limit is not None
                and len(all_listings) >= limit
            ):

                print(
                    f"\nReached test limit "
                    f"of {limit} listings."
                )

                return all_listings

        page += 1

        time.sleep(1)

    return all_listings


# ---------------------------------------------------------
# REMOVE DUPLICATES
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":

    limit = None

    # -----------------------------------------------------
    # Read --limit
    # -----------------------------------------------------

    if len(sys.argv) == 3:

        if sys.argv[1] != "--limit":

            print(
                "Usage:"
            )

            print(
                "python olx_detail_scraper.py"
            )

            print(
                "python olx_detail_scraper.py "
                "--limit 10"
            )

            sys.exit(1)

        try:

            limit = int(
                sys.argv[2]
            )

        except ValueError:

            print(
                "Limit must be a number."
            )

            sys.exit(1)

        if limit <= 0:

            print(
                "Limit must be greater than 0."
            )

            sys.exit(1)

    elif len(sys.argv) != 1:

        print(
            "Usage:"
        )

        print(
            "python olx_detail_scraper.py"
        )

        print(
            "python olx_detail_scraper.py "
            "--limit 10"
        )

        sys.exit(1)

    # -----------------------------------------------------
    # Collect listing URLs
    # -----------------------------------------------------

    listings = get_listing_urls(
        limit=limit
    )

    # -----------------------------------------------------
    # Remove duplicate URLs
    # -----------------------------------------------------

    unique_listings = remove_duplicates(
        listings
    )

    print("\n---")

    print(
        f"Total scraped listing URLs: "
        f"{len(listings)}"
    )

    print(
        f"Unique listing URLs: "
        f"{len(unique_listings)}"
    )

    # -----------------------------------------------------
    # Scrape details
    # -----------------------------------------------------

    print(
        "\nStarting detail scraping..."
    )

    detailed_listings = []

    total = len(unique_listings)

    for index, listing in enumerate(
        unique_listings,
        start=1
    ):

        url = listing["url"]

        external_id = listing[
            "external_id"
        ]

        print(
            f"\n[{index}/{total}] Scraping:"
        )

        print(url)

        try:

            detailed_listing = scrape_details(
                url
            )

            if detailed_listing:

                detailed_listings.append(
                    detailed_listing
                )

                print(
                    f"Successfully scraped "
                    f"{external_id}"
                )

            else:

                print(
                    f"Failed to scrape "
                    f"{external_id}"
                )

        except requests.exceptions.RequestException as e:

            print(
                f"Request failed for "
                f"{external_id}:"
            )

            print(e)

        except (
            KeyError,
            TypeError,
            json.JSONDecodeError
        ) as e:

            print(
                f"Failed to parse "
                f"{external_id}:"
            )

            print(e)

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

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

                print(
                    f"{key}: {value}"
                )