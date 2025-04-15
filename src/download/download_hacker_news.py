import pandas as pd
from sqlalchemy import create_engine, text, event
import os
import logging
import time
import backoff  # You may need to install this: pip install backoff
import traceback

# Fix import issue by using relative import path
try:
    from src.config import (
        DATA_DIR, HACKER_NEWS_DATASET_PATH, DB_CONNECTION_STRING, 
        BATCH_SIZE, ensure_directories
    )
except ModuleNotFoundError:
    # When running as a script directly
    from config import (
        DATA_DIR, HACKER_NEWS_DATASET_PATH, DB_CONNECTION_STRING, 
        BATCH_SIZE, ensure_directories
    )

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def get_db_engine():
    """Create a database engine with optimized connection settings."""
    # Database connection string with timeout parameters
    connection_string = DB_CONNECTION_STRING
    
    # Create engine with connection pooling and longer timeouts
    engine = create_engine(
        connection_string,
        pool_size=1,  # Use single connection for consistency
        pool_timeout=60,  # Wait up to 60 seconds for a connection
        connect_args={
            "connect_timeout": 120,  # Wait up to 2 minutes when connecting
            "options": "-c statement_timeout=900000"  # Set statement timeout to 15 minutes
        }
    )
    
    return engine

@backoff.on_exception(backoff.expo, Exception, max_tries=5)
def execute_query(query, engine=None):
    """Execute a query with retry logic."""
    close_engine = False
    if engine is None:
        engine = get_db_engine()
        close_engine = True
    
    try:
        logger.info("Executing query...")
        result = pd.read_sql_query(text(query), engine)
        logger.info(f"Query completed successfully, fetched {len(result)} rows.")
        return result
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise
    finally:
        if close_engine:
            engine.dispose()
            logger.info("Database connection closed")

def fetch_data_in_batches(output_file=HACKER_NEWS_DATASET_PATH, batch_size=BATCH_SIZE, max_batches=None):
    """Fetch the entire joined dataset in batches and write directly to CSV."""
    # Base query for the joined tables
    base_query = """
    SELECT 
        i.id AS item_id,
        i.type,
        i.title,
        i.score,
        i.time,
        i.url,
        i.text,
        i.by AS author_id,
        i.descendants AS comment_count,
        u.created AS user_created,
        u.karma AS user_karma,
        u.about AS user_about
    FROM 
        hacker_news.items i
    LEFT JOIN 
        hacker_news.users u ON i.by = u.id
    WHERE 
        i.type = 'story'
        AND i.title IS NOT NULL
    """
    
    # Ensure directories exist
    ensure_directories()
    
    engine = get_db_engine()
    
    try:
        # Get the total number of rows for progress tracking
        count_query = """
        SELECT COUNT(*) AS count
        FROM 
            hacker_news.items i
        WHERE 
            i.type = 'story'
            AND i.title IS NOT NULL
        """
        try:
            total_count_df = pd.read_sql_query(text(count_query), engine)
            total_count = total_count_df['count'].iloc[0]
            logger.info(f"Total rows to fetch: approximately {total_count}")
        except Exception as e:
            logger.warning(f"Could not get total count: {str(e)}")
            total_count = "unknown"
        
        # Start fetching data in batches
        offset = 0
        batch_num = 0
        total_rows = 0
        header = True
        
        while max_batches is None or batch_num < max_batches:
            batch_query = f"{base_query} ORDER BY i.id LIMIT {batch_size} OFFSET {offset}"
            
            try:
                logger.info(f"Fetching batch {batch_num+1} (offset {offset})...")
                batch_start = time.time()
                
                # Execute the query for this batch
                batch_df = pd.read_sql_query(text(batch_query), engine)
                
                batch_end = time.time()
                logger.info(f"Batch {batch_num+1} fetched {len(batch_df)} rows in {batch_end - batch_start:.2f} seconds")
                
                if len(batch_df) == 0:
                    logger.info("No more rows to fetch. Completed.")
                    break
                
                # Write this batch to the CSV file
                batch_df.to_csv(
                    output_file,
                    mode='w' if header else 'a',
                    header=header,
                    index=False
                )
                
                header = False  # Don't write header for subsequent batches
                total_rows += len(batch_df)
                batch_num += 1
                
                logger.info(f"Progress: {total_rows} rows fetched so far " + 
                           (f"({total_rows/total_count*100:.2f}%)" if isinstance(total_count, (int, float)) else ""))
                
                # Move to the next batch
                offset += batch_size
                
                # Small pause between batches to avoid overwhelming the server
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error fetching batch {batch_num+1}: {str(e)}")
                logger.error(traceback.format_exc())
                
                # If we've already fetched some batches, we can continue from where we left off
                if batch_num > 0:
                    logger.info(f"Retrying in 10 seconds from offset {offset}...")
                    time.sleep(10)
                    continue
                else:
                    raise
        
        logger.info(f"Data extraction completed. Total {total_rows} rows saved to {output_file}")
        return total_rows
        
    except Exception as e:
        logger.error(f"Fatal error in data extraction: {str(e)}")
        logger.error(traceback.format_exc())
        raise
    finally:
        engine.dispose()
        logger.info("Database connection closed")

def run_extraction():
    try:
        total_rows = fetch_data_in_batches()
        logger.info(f"Successfully extracted {total_rows} rows to {HACKER_NEWS_DATASET_PATH}")
        return total_rows
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        return 0

if __name__ == "__main__":
    run_extraction() 