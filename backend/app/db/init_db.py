# File: backend/app/db/init_db.py
"""
Database initialization and connection management.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..core.config import settings
from ..models.journal import Base, JournalEntry
from sqlalchemy.schema import MetaData

# Create synchronous engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# Create synchronous session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database with required tables."""
    # First create pgvector extension
    with engine.begin() as conn:
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
    
    # Then create tables
    Base.metadata.create_all(bind=engine)

def reset_database():
    """Drop all tables and recreate them"""
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        
        # Create pgvector extension
        with engine.begin() as conn:
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
            
            # Explicitly drop the table if it exists
            conn.execute(text('DROP TABLE IF EXISTS journal_entries CASCADE'))
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify table creation
        with engine.begin() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            print(f"Tables after reset: {tables}")
            
            # Verify columns in journal_entries
            if 'journal_entries' in tables:
                result = conn.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'journal_entries'
                """))
                columns = [f"{row[0]}: {row[1]}" for row in result]
                print(f"Journal entries columns: {columns}")
        
        return True
    except Exception as e:
        print(f"Error resetting database: {e}")
        raise e

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_database():
    """Verify database connection and tables."""
    try:
        with engine.connect() as conn:
            # Check pgvector extension
            conn.execute(text("SELECT * FROM pg_extension WHERE extname = 'vector'"))
            
            # Check tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            print(f"Found tables: {tables}")
            
            if 'journal_entries' in tables:
                result = conn.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'journal_entries'
                """))
                columns = [f"{row[0]}: {row[1]}" for row in result]
                print(f"Journal entries columns: {columns}")
                
        return True
    except Exception as e:
        print(f"Database verification failed: {e}")
        return False

# Add this function to test database connection
def test_db_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

# Add this to your startup
if __name__ == "__main__":
    test_db_connection()