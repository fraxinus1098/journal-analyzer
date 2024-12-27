from app.db.init_db import init_db, engine, get_db
from app.models.journal import JournalEntry
from app.utils.vector_utils import create_vector_similarity_index
import numpy as np
from sqlalchemy import text

def test_database_connection():
    print("\n1. Testing database connection...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print("❌ Database connection failed:", str(e))
        return False

def test_pgvector_extension():
    print("\n2. Testing pgvector extension...")
    try:
        with engine.connect() as conn:
            # Check if extension exists
            result = conn.execute(text("SELECT * FROM pg_extension WHERE extname = 'vector'")).scalar()
            if not result:
                print("❌ pgvector extension is not installed!")
                return False
            
            # Test vector operations are working
            test_query = text("SELECT '[1,2,3]'::vector <-> '[4,5,6]'::vector")
            conn.execute(test_query)
            print("✅ pgvector extension is installed and working!")
            return True
    except Exception as e:
        print("❌ Error checking pgvector:", str(e))
        return False

def test_table_creation():
    print("\n3. Testing table creation...")
    try:
        init_db()
        with engine.connect() as conn:
            # Verify journal_entries table exists
            result = conn.execute(text(
                "SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = 'journal_entries')"
            )).scalar()
            if not result:
                print("❌ journal_entries table not found!")
                return False
            print("✅ Tables created successfully!")
            return True
    except Exception as e:
        print("❌ Table creation failed:", str(e))
        return False

def test_vector_operations():
    print("\n4. Testing vector operations...")
    try:
        # Get a database session
        db = next(get_db())
        
        # Create a test entry with a random embedding
        test_embedding = np.random.rand(1536).astype(np.float32).tolist()
        test_entry = JournalEntry(
            content="Test entry",
            embedding=test_embedding
        )
        
        # Add and commit the test entry
        db.add(test_entry)
        db.commit()
        
        # Verify the entry was saved with the correct embedding
        saved_entry = db.query(JournalEntry).first()
        if not saved_entry or len(saved_entry.embedding) != 1536:
            print("❌ Vector storage verification failed!")
            return False
        
        # Test vector similarity search with proper PostgreSQL vector casting syntax
        query = text("""
            SELECT id FROM journal_entries 
            ORDER BY embedding <-> cast(:embedding as vector)
            LIMIT 1
        """)
        result = db.execute(query, {
            "embedding": f"[{','.join(map(str, test_embedding))}]"
        }).scalar()
        
        if not result:
            print("❌ Vector similarity search failed!")
            return False
        
        print("✅ Vector operations successful!")
        
        # Clean up
        db.delete(test_entry)
        db.commit()
        db.close()
        return True
        
    except Exception as e:
        print("❌ Vector operations failed:", str(e))
        return False

def test_vector_index():
    print("\n5. Testing vector index...")
    try:
        with engine.connect() as conn:
            # Check if the vector index exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM pg_indexes 
                    WHERE indexname = 'journal_entries_embedding_idx'
                )
            """)).scalar()
            if not result:
                print("❌ Vector index not found!")
                return False
            print("✅ Vector index exists!")
            return True
    except Exception as e:
        print("❌ Error checking vector index:", str(e))
        return False

def main():
    print("Starting database setup verification...\n")
    
    all_tests = [
        test_database_connection,
        test_pgvector_extension,
        test_table_creation,
        test_vector_operations,
        test_vector_index
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