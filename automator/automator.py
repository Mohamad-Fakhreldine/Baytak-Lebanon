from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import subprocess
import sys
import time

PROJECT_ROOT = Path(__file__).parent.parent
SCRAPER_PATH = PROJECT_ROOT / "scraper" / "run_scraper.py"
TIMEZONE = ZoneInfo("Asia/Beirut")

def get_next_midnight():
    now = datetime.now(TIMEZONE)
    next_day = now.date() + timedelta(days=1)
    return datetime(
        next_day.year,
        next_day.month,
        next_day.day,
        tzinfo=TIMEZONE,
    )
def wait_until_next_midnight():
    next_midnight = get_next_midnight()
    now = datetime.now(TIMEZONE)
    seconds_until_midnight = (
        next_midnight - now
    ).total_seconds()
    print(
        f"Next scraper run: "
        f"{next_midnight.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
    print(
        f"Waiting {seconds_until_midnight:.0f} seconds..."
    )
    time.sleep(seconds_until_midnight)
def run_scraper():
    print("\n==============================")
    print("STARTING DAILY SCRAPER")
    print("==============================")
    print(
        datetime.now(TIMEZONE).strftime(
            "Started: %Y-%m-%d %H:%M:%S %Z"
        )
    )
    result = subprocess.run(
        [sys.executable, str(SCRAPER_PATH)],
        cwd=PROJECT_ROOT,
    )
    print("\n==============================")
    print("DAILY SCRAPER FINISHED")
    print("==============================")
    print(f"Exit code: {result.returncode}")
    return result.returncode
def main():
    print("==============================")
    print("BAYTAK LEBANON AUTOMATOR")
    print("==============================")
    print("Timezone: Asia/Beirut")
    print("Schedule: Every day at midnight")
    print()
    while True:
        wait_until_next_midnight()
        run_scraper()
if __name__ == "__main__":
    main()