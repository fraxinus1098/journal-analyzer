from app.db.init_db import engine, init_db, SessionLocal
from app.utils.vector_utils import create_vector_similarity_index
from sqlalchemy import text
from app.models.journal import Base

def reset_database():
    # Drop all tables
    engine.dispose()
    with engine.connect() as conn:
        conn.execute(text('DROP EXTENSION IF EXISTS vector CASCADE'))
        conn.commit()
    
    # Drop and recreate all tables
    Base.metadata.drop_all(bind=engine)
    
    # Reinitialize everything
    init_db()
    
    # Create vector extension and index
    db = SessionLocal()
    try:
        db.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        db.commit()
        create_vector_similarity_index(db)
        print("Database reset successfully!")
    except Exception as e:
        print(f"Error during reset: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_database() 