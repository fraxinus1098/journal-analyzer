from database.init_db import init_db
from database.vector_ops import create_vector_similarity_index
from database.init_db import SessionLocal

def main():
    # Initialize database and create tables
    init_db()
    
    # Create vector similarity index
    db = SessionLocal()
    try:
        create_vector_similarity_index(db)
    finally:
        db.close()

if __name__ == "__main__":
    main() 