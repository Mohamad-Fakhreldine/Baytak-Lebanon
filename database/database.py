import sqlite3
from pathlib import Path


# Database location

DB_PATH = (
    Path(__file__).parent
    / "rental.db"
)


def create_database():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    cursor = connection.cursor()


    # ==========================
    # LISTINGS TABLE
    # ==========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS listings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            description TEXT,

            source TEXT NOT NULL,

            external_id TEXT NOT NULL,

            url TEXT NOT NULL,

            price REAL,

            currency TEXT,

            city TEXT,

            area TEXT,

            address TEXT,

            property_type TEXT,

            bedrooms INTEGER,

            bathrooms INTEGER,

            size REAL,

            furnished TEXT,

            seller_name TEXT,

            scraped_date TEXT NOT NULL,

            UNIQUE(source, external_id)

        )
        """
    )


    # ==========================
    # IMAGES TABLE
    # ==========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS images (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            listing_id INTEGER NOT NULL,

            image_url TEXT NOT NULL,

            image_order INTEGER,

            FOREIGN KEY (listing_id)
            REFERENCES listings(id)
            ON DELETE CASCADE

        )
        """
    )


    connection.commit()

    connection.close()


    print(
        "Database created successfully!"
    )


if __name__ == "__main__":

    create_database()