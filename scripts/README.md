# Scripts Directory

This directory contains utility scripts for the IndiaBixAuto project.

## Available Scripts

### mark_urls_as_scraped.py

This script marks a range of URLs as already scraped in MongoDB. It's useful for testing the URL skipping functionality in the workflow.

#### Usage

```bash
python mark_urls_as_scraped.py START_DATE END_DATE [MONGO_URI]
```

#### Example

To mark all URLs from May 1, 2025 to May 25, 2025 as scraped:

```bash
python mark_urls_as_scraped.py 2025-05-01 2025-05-25
```

If you need to specify a custom MongoDB URI:

```bash
python mark_urls_as_scraped.py 2025-05-01 2025-05-25 mongodb://username:password@localhost:27017
```

#### Environment Variables

The script will use the `MONGO_DB_URI` environment variable if no MongoDB URI is provided as an argument.

#### What It Does

1. Connects to the MongoDB database
2. For each date in the specified range:
   - Creates the URL in the format `https://www.indiabix.com/current-affairs/YYYY-MM-DD/`
   - Marks the URL as processed in the `scraped_urls` collection
   - Sets a dummy question count of 10 for each URL

#### Testing the Workflow

After running this script to mark URLs as scraped, you can test the GitHub Actions workflow by running:

```bash
python main.py --month 2025-05 --languages en gu --send-telegram --github-actions
```

The workflow should skip all the URLs that were marked as scraped and only process new URLs. 