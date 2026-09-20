import requests
import time
import sys
from pathlib import Path


# ---------------------------------------------------------
# Database module location
# ---------------------------------------------------------

DATABASE_PATH = (
    Path(__file__).parent.parent
    / "database"
)

sys.path.insert(
    0,
    str(DATABASE_PATH)
)


from temp_database import create_database


# ---------------------------------------------------------
# Scrapers
# ---------------------------------------------------------

from olx_scraper import (
    scrape_olx,
    remove_duplicates
)

from olx_detail_scraper import scrape_details


# ---------------------------------------------------------
# Database handler
# ---------------------------------------------------------

from database_handler import (
    get_connection,
    insert_listing
)


# ---------------------------------------------------------
# Temporary database location
# ---------------------------------------------------------

TEMP_DB_PATH = (
    DATABASE_PATH
    / "rental_temp.db"
)


def run():

    # ---------------------------------------------------------
    # Create a fresh temporary database
    # ---------------------------------------------------------

    if TEMP_DB_PATH.exists():

        TEMP_DB_PATH.unlink()

    create_database()

    # ---------------------------------------------------------
    # Get current listing URLs from OLX
    # ---------------------------------------------------------

    listings, scrape_complete = scrape_olx()

    listings = remove_duplicates(
        listings
    )

    total_listings = len(listings)

    print(
        "\nFound unique URLs:",
        total_listings
    )

    print(
        "OLX scrape complete:",
        scrape_complete
    )

    # ---------------------------------------------------------
    # Do not build a new database if OLX pagination
    # was incomplete.
    # ---------------------------------------------------------

    if not scrape_complete:

        print(
            "\nOLX scrape was incomplete."
        )

        print(
            "Aborting database rebuild."
        )

        return

    # ---------------------------------------------------------
    # Counters
    # ---------------------------------------------------------

    inserted_listings = 0
    failed = []

    # ---------------------------------------------------------
    # Open ONE database connection for the entire run
    # ---------------------------------------------------------

    connection = get_connection()

    cursor = connection.cursor()

    try:

        # -----------------------------------------------------
        # Scrape details and build the new database
        # -----------------------------------------------------

        for index, item in enumerate(
            listings,
            start=1
        ):

            external_id = item["external_id"]
            url = item["url"]

            print(
                f"\n[{index}/{total_listings}] "
                f"Scraping: {external_id}"
            )

            success = False

            # -------------------------------------------------
            # Try each listing up to 3 times
            # -------------------------------------------------

            for attempt in range(1, 4):

                try:

                    listing = scrape_details(
                        url
                    )

                    if listing:

                        # -------------------------------------
                        # Insert listing into the new database
                        # -------------------------------------

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

                # -------------------------------------------------
                # HTTP / network errors
                # -------------------------------------------------

                except requests.exceptions.RequestException as e:

                    print(
                        f"Attempt {attempt}/3 failed "
                        f"for {external_id}"
                    )

                    print(e)

                # -------------------------------------------------
                # Unexpected errors
                # -------------------------------------------------

                except Exception as e:

                    print(
                        f"Attempt {attempt}/3 encountered "
                        f"an unexpected error for "
                        f"{external_id}"
                    )

                    print(
                        f"{type(e).__name__}: {e}"
                    )

                # -------------------------------------------------
                # Retry delay
                # -------------------------------------------------

                if attempt < 3:

                    print(
                        "Retrying in 2 seconds..."
                    )

                    time.sleep(2)

            # -----------------------------------------------------
            # All 3 attempts failed
            # -----------------------------------------------------

            if not success:

                print(
                    f"\nFAILED AFTER 3 ATTEMPTS: "
                    f"{external_id}"
                )

                failed.append(
                    external_id
                )

        # ---------------------------------------------------------
        # Commit the newly built database
        # ---------------------------------------------------------

        connection.commit()

    except Exception:

        # ---------------------------------------------------------
        # Something unexpected happened while building
        # the new database.
        # ---------------------------------------------------------

        connection.rollback()

        raise

    finally:

        connection.close()

    # ---------------------------------------------------------
    # Final results
    # ---------------------------------------------------------

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
        f"{len(failed)}"
    )

    print(
        f"OLX scrape complete: "
        f"{scrape_complete}"
    )

    # ---------------------------------------------------------
    # Failed listings
    # ---------------------------------------------------------

    if failed:

        print("\nFailed external IDs:")

        for external_id in failed:

            print(
                external_id
            )

    else:

        print(
            "\nAll listings were successfully "
            "scraped and inserted!"
        )


if __name__ == "__main__":

    run()