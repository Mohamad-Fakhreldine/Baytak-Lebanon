import sqlite3
from pathlib import Path


DB_PATH = (
    Path(__file__).parent.parent
    / "database"
    / "rental_temp.db"
)


def get_connection():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def insert_listing(
    cursor,
    listing
):

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
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, datetime('now')
        )
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

    insert_images(
        cursor,
        listing_id,
        listing.get("images", [])
    )

    return listing_id


def update_listing(
    cursor,
    listing,
    listing_id
):

    cursor.execute(
        """
        UPDATE listings
        SET
            title = ?,
            description = ?,
            url = ?,
            price = ?,
            currency = ?,
            city = ?,
            area = ?,
            property_type = ?,
            bedrooms = ?,
            bathrooms = ?,
            size = ?,
            furnished = ?,
            seller_name = ?,
            scraped_date = datetime('now')
        WHERE id = ?
        """,
        (
            listing.get("title"),
            listing.get("description"),
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
            listing.get("seller_name"),
            listing_id
        )
    )

    # Remove the old image records.
    cursor.execute(
        """
        DELETE FROM images
        WHERE listing_id = ?
        """,
        (
            listing_id,
        )
    )

    # Insert the current images.
    insert_images(
        cursor,
        listing_id,
        listing.get("images", [])
    )


def insert_images(
    cursor,
    listing_id,
    images
):

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


def find_listing(
    cursor,
    source,
    external_id
):

    cursor.execute(
        """
        SELECT id
        FROM listings
        WHERE source = ?
        AND external_id = ?
        """,
        (
            source,
            external_id
        )
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return None

def get_listing_ids(
    cursor,
    source
):

    cursor.execute(
        """
        SELECT external_id
        FROM listings
        WHERE source = ?
        """,
        (
            source,
        )
    )

    return {
        row[0]
        for row in cursor.fetchall()
    }


def delete_listings(
    cursor,
    external_ids,
    source
):

    if not external_ids:
        return 0

    placeholders = ",".join(
        "?"
        for _ in external_ids
    )

    parameters = [
        source,
        *external_ids
    ]

    cursor.execute(
        f"""
        DELETE FROM listings
        WHERE source = ?
        AND external_id IN ({placeholders})
        """,
        parameters
    )

    return cursor.rowcount