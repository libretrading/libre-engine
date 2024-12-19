from sqlalchemy import Column, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# load .env variables
load_dotenv()

# Database configuration
DATABASE_URI = f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@" \
               f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

Base = declarative_base()

# Active Table (for active users)
class ActiveUser(Base):
    __tablename__ = 'active'
    email = Column(String, primary_key=True)
    api_public = Column(String)
    api_secret = Column(String)

# Inactive Table (for users who stopped the strategy)
class InactiveUser(Base):
    __tablename__ = 'inactive'
    email = Column(String, primary_key=True)
    api_public = Column(String)
    api_secret = Column(String)
    to_be_stopped = Column(Boolean, default=True)

# Create engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)