Lebanese Home Rental Aggregator
A web platform that aggregates Lebanese rental listings into one place.
The core of the project is an automated scraper and data pipeline that collects rental listings from OLX Lebanon, cleans and structures them, and stores them in a single database. Baytak Lebanon, the website built on top of it, lets visitors browse, filter, and save listings and follow a link to the original ad.
Full project documentation (requirements, design, implementation): see the Word document in the docs/ folder.

Features
·	Automated scraping. Every rental listing on OLX Lebanon is collected every night at midnight (Asia/Beirut time).
·	Data cleaning. A bilingual (English and Arabic), rule-based parser fills missing bedrooms, bathrooms, and size from the listing description when OLX's own fields are empty.
·	Duplicate prevention. One entry is kept per source and external ID, in both the scraper and the database.
·	Safe refresh. Each run builds a brand-new database, validates it, and swaps it in atomically. A failed or incomplete run never touches the live data.
·	Website.
o	Paginated listings with filters: location, property type, price range, size range, and furnishing.
o	Listing details popup with a "Go to source" button.
o	Save listings with a heart icon, with no account needed (stored in the browser).
o	Home, Listings, Saved, Contact Us, Privacy Policy, and About pages.
·	Extensible. Each source is its own scraper feeding the same database.
Tech stack
Layer	Technology
Scraping	Python, Playwright, Beautiful Soup, requests
Parsing	Python regular expressions
Database	SQLite
Backend	Flask, Flask-SQLAlchemy, Flask-CORS, Gunicorn
Frontend	React, Vite, Choices.js
Deployment	Docker, Docker Compose

Project structure
.
├── automator/      Scheduler: runs the scraper every day at midnight
├── backend/        Flask API and the backend Dockerfile
├── database/       SQLite files and the database scripts
├── frontend/       React website (Vite)
├── scraper/        Scraper, description parser, and the pipeline script
├── docs/           Project documentation
├── docker-compose.yml
└── requirements.txt

How it works
1.	At midnight, the automator starts the scraper pipeline.
2.	The pipeline creates a fresh rental_temp.db and collects all listing IDs and URLs from OLX's rental pages.
3.	Each listing page is fetched (up to 3 attempts), its fields are extracted, and missing details are recovered from the description.
4.	If the scrape completed, at least one listing was found, and no more than 5% of listings failed, rental_temp.db replaces rental.db in one atomic step. Otherwise the existing live database is kept.
5.	The Flask backend serves the live database to the React frontend.
A full run takes about 3 hours.

Getting started
Requirements
·	Docker with Docker Compose
1. Clone the repository
git clone <repository-url>
cd <repository-folder>

2. Build the images
docker compose build

3. Build the database for the first time
The scraper runs automatically at midnight, so a fresh install has no data until then. To fill the database right away, run the pipeline once by hand:
docker compose run --rm automator python /app/scraper/run_scraper.py

This takes about 3 hours. When it finishes, the new database is swapped in as database/rental.db.
4. Start the project
docker compose up -d

Open http://localhost in your browser.
From now on the automator container refreshes the data every night at midnight (Asia/Beirut time). The first scheduled run happens at the next midnight after the containers start, not at startup.
Everyday commands
Task	Command
Start in the background	docker compose up -d
Start and rebuild after code changes	docker compose up -d --build
Follow the scraper's logs	docker compose logs -f automator
Follow the API's logs	docker compose logs -f backend
Stop everything	docker compose down
Run the scraper manually	docker compose run --rm automator python /app/scraper/run_scraper.py

Running without Docker (development)
Requires Python 3.12 and Node.js.
# Python dependencies
pip install -r requirements.txt
playwright install chromium

# Backend (http://localhost:5000)
cd backend
python app.py

# Frontend (in a second terminal)
cd frontend
npm install
npm run dev

The frontend calls relative /api/... URLs, so the Vite dev server must proxy /api to http://localhost:5000.
Troubleshooting
·	The site shows no listings. The database has not been built yet. Run step 3 and wait for it to finish.
·	A run finished but the data did not change. The pipeline keeps the old database when the scrape is incomplete, no listings are found, or more than 5% of listings fail. Check docker compose logs automator for the reason.
·	The scraper fails at startup. OLX may have changed its page structure, and the scraper needs updating.
Limitations
·	Rental listings from OLX Lebanon only. Coverage means everything OLX lists, not every rental in Lebanon.
·	Duplicates are prevented within a source only. The same property posted as separate ads, or on other platforms, is not detected.
·	Data is refreshed once a day, so a removed or edited listing can stay visible for up to about 24 hours.
·	Saved listings live in the browser, so they do not sync across devices.
·	The layout is built for desktop screens.
See the documentation for the full list of future improvements.
Disclaimer
This is a personal portfolio project. All listing data comes from OLX Lebanon and remains the property of its respective owners. Every listing links back to its original source.
Author
Mohamad Jawad Fakhreldine

Email: mohamad.jawad.fakhreldine.dev@gmail.com
GitHub: https://github.com/Mohamad-Fakhreldine
License
