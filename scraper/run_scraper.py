import requests
import time

from olx_scraper import scrape_olx
from olx_detail_scraper import scrape_details
from database_handler import insert_listing


def run():

    # ---------------------------------------------------------
    # Get ALL listing URLs from OLX
    # ---------------------------------------------------------

    listings = scrape_olx()

    total_listings = len(listings)

    print(
        "\nFound URLs:",
        total_listings
    )

    # ---------------------------------------------------------
    # Counters
    # ---------------------------------------------------------

    successful = 0
    failed = []

    # ---------------------------------------------------------
    # Scrape details and insert into database
    # ---------------------------------------------------------

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

        # -----------------------------------------------------
        # Try each listing up to 3 times
        # -----------------------------------------------------

        for attempt in range(1, 4):

            try:

                listing = scrape_details(
                    url
                )

                if listing:

                    insert_listing(
                        listing
                    )

                    successful += 1
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
    # Final results
    # ---------------------------------------------------------

    print("\n")
    print("==============================")
    print("SCRAPING COMPLETE")
    print("==============================")

    print(
        f"Total listings found: {total_listings}"
    )

    print(
        f"Successfully inserted: {successful}"
    )

    print(
        f"Failed after 3 attempts: {len(failed)}"
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