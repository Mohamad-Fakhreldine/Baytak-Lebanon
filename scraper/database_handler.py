import sqlite3
from pathlib import Path


DB_PATH = (
    Path(__file__).parent.parent
    / "database"
    / "rental.db"
)


def insert_listing(listing):

    connection = sqlite3.connect(DB_PATH)

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    cursor = connection.cursor()

    # ---------------------------------------------------------
    # Check whether this listing already exists
    # ---------------------------------------------------------

    cursor.execute(
        """
        SELECT id
        FROM listings
        WHERE source = ?
        AND external_id = ?
        """,
        (
            listing["source"],
            listing["external_id"]
        )
    )

    existing = cursor.fetchone()

    if existing:

        print(
            f"Listing {listing['external_id']} "
            f"already exists. Skipping."
        )

        connection.close()

        return False

    # ---------------------------------------------------------
    # Insert listing
    # ---------------------------------------------------------

    cursor.execute(
        """
        INSERT INTO listings (
            title,
            description,
            source,
            external_id,
            url,
            price,
            currency,
            city,
            area,
            property_type,
            bedrooms,
            bathrooms,
            size,
            furnished,
            seller_name,
            scraped_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            listing.get("title"),
            listing.get("description"),
            listing.get("source"),
            listing.get("external_id"),
            listing.get("url"),
            listing.get("price"),
            listing.get("currency"),
            listing.get("city"),
            listing.get("area"),
            listing.get("property_type"),
            listing.get("bedrooms"),
            listing.get("bathrooms"),
            listing.get("size"),
            listing.get("furnished"),
            listing.get("seller_name")
        )
    )

    listing_id = cursor.lastrowid

    print(
        f"Inserted listing "
        f"{listing['external_id']}"
    )

    # ---------------------------------------------------------
    # Insert images
    # ---------------------------------------------------------

    images = listing.get(
        "images",
        []
    )

    for image_order, image_url in enumerate(
        images,
        start=1
    ):

        cursor.execute(
            """
            INSERT INTO images (
                listing_id,
                image_url,
                image_order
            )
            VALUES (?, ?, ?)
            """,
            (
                listing_id,
                image_url,
                image_order
            )
        )

    print(
        f"Images inserted: "
        f"{len(images)}"
    )

    connection.commit()

    connection.close()

    return True