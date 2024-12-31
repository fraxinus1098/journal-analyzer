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

def check_table_structure():
    """Check the actual structure of the journal_entries table"""
    try:
        with engine.connect() as conn:
            # Check if table exists
            table_exists = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'journal_entries'
                );
            """)).scalar()
            
            print(f"Table exists: {table_exists}")
            
            if table_exists:
                # Get all columns and their types
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'journal_entries'
                    ORDER BY ordinal_position;
                """))
                
                columns = [f"{row[0]} ({row[1]}, nullable: {row[2]})" for row in result]
                print("Table structure:")
                for col in columns:
                    print(f"  - {col}")
            
            return table_exists
    except Exception as e:
        print(f"Error checking table structure: {e}")
        return False

def reset_database():
    """Drop all tables and recreate them"""
    try:
        print("\n=== Starting Database Reset ===")
        
        # Create a new connection
        conn = engine.raw_connection()
        cursor = conn.cursor()
        
        try:
            # Drop everything
            cursor.execute('DROP SCHEMA public CASCADE')
            cursor.execute('CREATE SCHEMA public')
            cursor.execute('GRANT ALL ON SCHEMA public TO postgres')
            cursor.execute('GRANT ALL ON SCHEMA public TO public')
            print("✓ Reset schema")
            
            # Recreate vector extension
            cursor.execute('CREATE EXTENSION IF NOT EXISTS vector')
            print("✓ Created pgvector extension")
            
            # Commit these changes
            conn.commit()
            
            # Create all tables from models
            Base.metadata.create_all(bind=engine)
            print("✓ Created all tables")
            
            # Verify table structure
            print("\n=== Verifying Table Structure ===")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'journal_entries'
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            print("Table structure:")
            for col in columns:
                print(f"  - {col[0]} ({col[1]}, nullable: {col[2]})")
            
            print("=== Database Reset Complete ===\n")
            
        finally:
            cursor.close()
            conn.close()
            
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