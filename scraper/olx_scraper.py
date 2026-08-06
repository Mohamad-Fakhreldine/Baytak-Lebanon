import requests
from bs4 import BeautifulSoup


url = "https://olx.com.lb/properties/beirut/?page=2&filter=price_between_300_to_500"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "Chrome/120 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

html = response.text

soup = BeautifulSoup(html, "lxml")

listings = soup.find_all("li", attrs={"aria-label": "Listing"})

print("Listings found:", len(listings))


for listing in listings[:3]:
    print("\n--- LISTING ---")

    title = listing.find("h2")
    print("Title:", title.text.strip() if title else None)

    price = listing.find(attrs={"aria-label": "Price"})
    print("Price:", price.text.strip() if price else None)

    location = listing.find(attrs={"aria-label": "Location"})
    print("Location:", location.text.strip() if location else None)