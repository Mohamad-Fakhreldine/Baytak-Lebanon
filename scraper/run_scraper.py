import os
import requests
import time
import sys
from pathlib import Path

DATABASE_PATH = (
    Path(__file__).parent.parent
    / "database"
)

sys.path.insert(
    0,
    str(DATABASE_PATH)
)

from temp_database import create_database

from olx_scraper import (
    scrape_olx,
    remove_duplicates
)

from olx_detail_scraper import scrape_details

from database_handler import (
    get_connection,
    insert_listing
)

TEMP_DB_PATH = (
    DATABASE_PATH
    / "rental_temp.db"
)

LIVE_DB_PATH = (
    DATABASE_PATH
    / "rental.db"
)

MAX_FAILURE_RATE = 0.01


def run():

    if TEMP_DB_PATH.exists():
        print("\nRemoving existing temporary database...")
        TEMP_DB_PATH.unlink()

    print("\nCreating temporary database...")
    create_database()

    listings, scrape_complete = scrape_olx()
    listings = remove_duplicates(listings)

    total_listings = len(listings)

    print("\nFound unique URLs:", total_listings)
    print("OLX scrape complete:", scrape_complete)

    if not scrape_complete:
        print("\nOLX scrape was incomplete.")
        print("Aborting database rebuild.")
        return

    inserted_listings = 0
    failed = []

    connection = get_connection()
    cursor = connection.cursor()

    try:

        for index, item in enumerate(listings, start=1):

            external_id = item["external_id"]
            url = item["url"]

            print(
                f"\n[{index}/{total_listings}] "
                f"Scraping: {external_id}"
            )

            success = False

            for attempt in range(1, 4):

                try:

                    listing = scrape_details(url)

                    if listing:

                        insert_listing(
                            cursor,
                            listing
                        )

                        inserted_listings += 1

                        print(
                            f"Listing inserted: "
                            f"{external_id}"
                        )

                        success = True
                        break

                    else:

                        print(
                            f"Attempt {attempt}/3 failed "
                            f"for {external_id}: "
                            f"No listing data returned."
                        )

                except requests.exceptions.RequestException as e:

                    print(
                        f"Attempt {attempt}/3 failed "
                        f"for {external_id}"
                    )

                    print(e)

                except Exception as e:

                    print(
                        f"Attempt {attempt}/3 encountered "
                        f"an unexpected error for "
                        f"{external_id}"
                    )

                    print(
                        f"{type(e).__name__}: {e}"
                    )

                if attempt < 3:

                    print(
                        "Retrying in 2 seconds..."
                    )

                    time.sleep(2)

            if not success:

                print(
                    f"\nFAILED AFTER 3 ATTEMPTS: "
                    f"{external_id}"
                )

                failed.append(external_id)

        connection.commit()

    except Exception:

        connection.rollback()

        print(
            "\nA database or system error occurred."
        )

        print(
            "Aborting database rebuild."
        )

        raise

    finally:

        connection.close()

    failed_count = len(failed)

    failure_rate = (
        failed_count / total_listings
        if total_listings > 0
        else 1
    )

    print("\n")
    print("==============================")
    print("DATABASE BUILD COMPLETE")
    print("==============================")

    print(
        f"Total listings found: "
        f"{total_listings}"
    )

    print(
        f"Listings inserted: "
        f"{inserted_listings}"
    )

    print(
        f"Failed after 3 attempts: "
        f"{failed_count}"
    )

    print(
        f"Failure rate: "
        f"{failure_rate:.2%}"
    )

    print(
        f"Maximum allowed failure rate: "
        f"{MAX_FAILURE_RATE:.2%}"
    )

    print(
        f"OLX scrape complete: "
        f"{scrape_complete}"
    )

    if failed:

        print("\nFailed external IDs:")

        for external_id in failed:
            print(external_id)

    if failure_rate > MAX_FAILURE_RATE:

        print(
            "\nFailure rate exceeded the allowed "
            "threshold."
        )

        print(
            "Keeping the existing live database."
        )

        print(
            "Temporary database will be removed."
        )

        if TEMP_DB_PATH.exists():
            TEMP_DB_PATH.unlink()

        return

    if total_listings == 0:

        print(
            "\nNo listings were found."
        )

        print(
            "Keeping the existing live database."
        )

        print(
            "Temporary database will be removed."
        )

        if TEMP_DB_PATH.exists():
            TEMP_DB_PATH.unlink()

        return

    print(
        "\nValidation passed."
    )

    print(
        "Replacing live database..."
    )

    os.replace(
        TEMP_DB_PATH,
        LIVE_DB_PATH
    )

    print(
        "Atomic database swap completed successfully."
    )

    print(
        "New database is now live."
    )


if __name__ == "__main__":
    run()