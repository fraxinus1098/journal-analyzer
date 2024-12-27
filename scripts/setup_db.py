from app.db.init_db import init_db
from app.utils.vector_utils import create_vector_similarity_index
from app.db.init_db import SessionLocal
from sqlalchemy import text

def main():
    # Initialize database and create tables
    init_db()
    
    # Create vector extension
    db = SessionLocal()
    try:
        db.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        db.commit()
        print("Vector extension created successfully!")
        
        # Create vector similarity index
        create_vector_similarity_index(db)
        print("Vector similarity index created successfully!")
    except Exception as e:
        print(f"Error during setup: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 