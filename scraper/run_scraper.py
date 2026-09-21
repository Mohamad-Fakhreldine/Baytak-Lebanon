import os
import requests
import time
import sys
from pathlib import Path
DATABASE_PATH = Path(__file__).parent.parent / "database"
TEMP_DB_PATH = DATABASE_PATH / "rental_temp.db"
LIVE_DB_PATH = DATABASE_PATH / "rental.db"
MAX_FAILURE_RATE = 0.05
sys.path.insert(0, str(DATABASE_PATH))
from temp_database import create_database
from database_handler import get_connection, insert_listing
from olx_scraper import scrape_olx, remove_duplicates
from olx_detail_scraper import scrape_details

def remove_temp_database():
    if TEMP_DB_PATH.exists():
        TEMP_DB_PATH.unlink()

def scrape_listing(url, external_id, cursor):
    for attempt in range(1, 4):
        try:
            listing = scrape_details(url)
            if listing:
                insert_listing(cursor, listing)
                print(f"Listing inserted: {external_id}")
                return True
            print(
                f"Attempt {attempt}/3 failed for "
                f"{external_id}: No listing data returned."
            )
        except requests.exceptions.RequestException as e:
            print(
                f"Attempt {attempt}/3 failed for "
                f"{external_id}: {e}"
            )
        except Exception as e:
            print(
                f"Attempt {attempt}/3 encountered an "
                f"unexpected error for {external_id}"
            )
            print(f"{type(e).__name__}: {e}")
        if attempt < 3:
            print("Retrying in 2 seconds...")
            time.sleep(2)
    print(f"\nFAILED AFTER 3 ATTEMPTS: {external_id}")
    return False

def build_database(listings):
    inserted_listings = 0
    failed = []
    connection = get_connection()
    cursor = connection.cursor()
    try:
        total_listings = len(listings)

        for index, item in enumerate(listings, start=1):
            external_id = item["external_id"]
            url = item["url"]
            print(
                f"\n[{index}/{total_listings}] "
                f"Scraping: {external_id}"
            )
            if scrape_listing(url, external_id, cursor):
                inserted_listings += 1
            else:
                failed.append(external_id)
        connection.commit()
    except Exception:
        connection.rollback()
        print("\nA database or system error occurred.")
        print("Aborting database rebuild.")
        raise
    finally:
        connection.close()
    return inserted_listings, failed

def calculate_failure_rate(failed_count, total_listings):
    if total_listings == 0:
        return 1
    return failed_count / total_listings

def print_results(
    total_listings,
    inserted_listings,
    failed,
    failure_rate,
    scrape_complete
):
    print("\n==============================")
    print("DATABASE BUILD COMPLETE")
    print("==============================")
    print(f"Total listings found: {total_listings}")
    print(f"Listings inserted: {inserted_listings}")
    print(f"Failed after 3 attempts: {len(failed)}")
    print(f"Failure rate: {failure_rate:.2%}")
    print(
        f"Maximum allowed failure rate: "
        f"{MAX_FAILURE_RATE:.2%}"
    )
    print(f"OLX scrape complete: {scrape_complete}")
    if failed:
        print("\nFailed external IDs:")

        for external_id in failed:
            print(external_id)

def run():
    remove_temp_database()
    print("\nCreating temporary database...")
    create_database()
    listings, scrape_complete = scrape_olx()
    listings = remove_duplicates(listings)
    total_listings = len(listings)
    print(f"\nFound unique URLs: {total_listings}")
    print(f"OLX scrape complete: {scrape_complete}")
    if not scrape_complete:
        print("\nOLX scrape was incomplete.")
        print("Aborting database rebuild.")
        remove_temp_database()
        return
    inserted_listings, failed = build_database(listings)
    failure_rate = calculate_failure_rate(
        len(failed),
        total_listings
    )
    print_results(
        total_listings,
        inserted_listings,
        failed,
        failure_rate,
        scrape_complete
    )
    if failure_rate > MAX_FAILURE_RATE:
        print("\nFailure rate exceeded the allowed threshold.")
        print("Keeping the existing live database.")
        print("Temporary database will be removed.")
        remove_temp_database()
        return
    if total_listings == 0:
        print("\nNo listings were found.")
        print("Keeping the existing live database.")
        print("Temporary database will be removed.")
        remove_temp_database()
        return
    print("\nValidation passed.")
    print("Replacing live database...")
    os.replace(
        TEMP_DB_PATH,
        LIVE_DB_PATH
    )
    print("Atomic database swap completed successfully.")
    print("New database is now live.")
if __name__ == "__main__":
    run()