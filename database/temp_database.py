import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).parent / "rental_temp.db"
def create_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(
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
        connection.execute(
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
    print("Database created successfully!")
if __name__ == "__main__":
    create_database()