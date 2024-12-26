from database.init_db import init_db, engine, get_db
from database.models import JournalEntry
from database.vector_ops import create_vector_similarity_index
import numpy as np

def test_database_connection():
    print("\n1. Testing database connection...")
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1").scalar()
            print("✅ Database connection successful!")
    except Exception as e:
        print("❌ Database connection failed:", str(e))
        return False

def test_pgvector_extension():
    print("\n2. Testing pgvector extension...")
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT * FROM pg_extension WHERE extname = 'vector'").scalar()
            if result:
                print("✅ pgvector extension is installed!")
            else:
                print("❌ pgvector extension is not installed!")
                return False
    except Exception as e:
        print("❌ Error checking pgvector:", str(e))
        return False

def test_table_creation():
    print("\n3. Testing table creation...")
    try:
        init_db()
        print("✅ Tables created successfully!")
    except Exception as e:
        print("❌ Table creation failed:", str(e))
        return False

def test_vector_operations():
    print("\n4. Testing vector operations...")
    try:
        # Get a database session
        db = next(get_db())
        
        # Create a test entry with a random embedding
        test_embedding = np.random.rand(1536).tolist()  # OpenAI embeddings are 1536-dimensional
        test_entry = JournalEntry(
            content="Test entry",
            embedding=test_embedding
        )
        
        # Add and commit the test entry
        db.add(test_entry)
        db.commit()
        
        # Create the vector similarity index
        create_vector_similarity_index(db)
        
        print("✅ Vector operations successful!")
        
        # Clean up
        db.delete(test_entry)
        db.commit()
        db.close()
        
    except Exception as e:
        print("❌ Vector operations failed:", str(e))
        return False

def main():
    print("Starting database setup verification...\n")
    
    all_tests = [
        test_database_connection,
        test_pgvector_extension,
        test_table_creation,
        test_vector_operations
    ]
    
    success = True
    for test in all_tests:
        if test() is False:
            success = False
            break
    
    if success:
        print("\n✨ All database tests passed! Your setup is complete!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 