from sqlalchemy import create_engine, MetaData, Table, update
from dotenv import load_dotenv
import pandas as pd
import os

# load .env variables
load_dotenv()

# PostgreSQL configuration
DATABASE_URI = f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@" \
               f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

engine = create_engine(DATABASE_URI)
# Define the table metadata
metadata = MetaData()

# Define the inactive table (make sure the column names match your database)
inactive_table = Table('inactive', metadata, autoload_with=engine)

def get_active_accounts():
    """Fetch active accounts from the database."""
    query = "SELECT * FROM active;"
    df = pd.read_sql(query, engine)
    return df.to_dict('records')

def get_inactive_accounts():
    """Fetch inactive accounts from the database."""
    query = "SELECT * FROM inactive;"
    df = pd.read_sql(query, engine)
    return df.to_dict('records')

def update_liquidation_status(account):
    # Use SQLAlchemy's update statement
    stmt = (
        update(inactive_table)
        .where(inactive_table.c.email == account['email'])  # Referring to the email column
        .values(to_be_stopped=False)  # Set the 'to_be_stopped' column to False
    )
                
    # Use the engine's connection to execute the update query and commit it
    with engine.begin() as conn:  # Use begin() to automatically commit the transaction
        conn.execute(stmt)
        print(f"Updated 'to_be_stopped' to false for {account['email']}")