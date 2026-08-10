import requests
import json
import sys
import time 

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

            return (
                data["props"]
                ["pageProps"]
                ["initialState"]
                ["ad"]
                ["data"]
            )

    return None


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
# EXTRACT IMAGES
# ---------------------------------------------------------

def extract_images(photos):

    images = []

    for photo in photos:

        image_id = photo.get("id")

        if image_id:

            images.append(
                f"https://images-prod.olx-dubizzle.com/"
                f"thumbnails/{image_id}-600x450.jpeg"
            )

    return images


# ---------------------------------------------------------
# SCRAPE ONE LISTING
# ---------------------------------------------------------

def scrape_details(url):

    ad = get_ad_data(url)

    if not ad:
        return None

    description = ad.get(
        "description"
    )

    formatted_fields = ad.get(
        "formattedExtraFields",
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
        ad.get("photos", [])
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