#!/usr/bin/env python
"""
Script to mark URLs as scraped in MongoDB.
This is useful for testing the URL skipping functionality.
"""

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))

from src.core.utils import setup_mongodb_connection, mark_url_as_processed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

async def mark_date_range_as_scraped(start_date: str, end_date: str, mongo_uri: str = None):
    """
    Mark a range of dates as scraped in MongoDB
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        mongo_uri: MongoDB URI
    """
    # Get MongoDB URI from environment if not provided
    if not mongo_uri:
        mongo_uri = os.environ.get("MONGO_DB_URI")
        if not mongo_uri:
            logger.error("MongoDB URI not provided. Set MONGO_DB_URI environment variable or pass as parameter.")
            return
    
    # Setup MongoDB connection
    mongo_connection = setup_mongodb_connection(mongo_uri)
    if not mongo_connection:
        logger.error("Failed to connect to MongoDB.")
        return
    
    # Convert dates to datetime objects
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Generate dates in the range
    current_dt = start_dt
    marked_count = 0
    
    while current_dt <= end_dt:
        date_str = current_dt.strftime("%Y-%m-%d")
        url = f"https://www.indiabix.com/current-affairs/{date_str}/"
        
        # Mark URL as processed
        success = mark_url_as_processed(mongo_connection, url, question_count=10)
        if success:
            logger.info(f"Marked URL as processed: {url}")
            marked_count += 1
        else:
            logger.error(f"Failed to mark URL as processed: {url}")
        
        # Move to next day
        current_dt += timedelta(days=1)
    
    logger.info(f"Successfully marked {marked_count} URLs as processed.")

def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python mark_urls_as_scraped.py START_DATE END_DATE [MONGO_URI]")
        print("Example: python mark_urls_as_scraped.py 2025-05-01 2025-05-25")
        return
    
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    mongo_uri = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Validate date format
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format.")
        return
    
    # Run async function
    asyncio.run(mark_date_range_as_scraped(start_date, end_date, mongo_uri))

if __name__ == "__main__":
    main() 