import numpy as np
from app.db.init_db import get_db
from app.models.journal import JournalEntry

def test_pgvector_insert():
    db = next(get_db())
    try:
        # Create a test vector
        test_vector = np.random.rand(1536).astype(np.float32)
        
        # Create and insert a test entry
        entry = JournalEntry(
            content="Test entry",
            embedding=test_vector.tolist()
        )
        db.add(entry)
        db.commit()
        
        # Verify the entry was saved
        saved_entry = db.query(JournalEntry).first()
        assert saved_entry is not None
        assert len(saved_entry.embedding) == 1536
        
    finally:
        # Cleanup
        db.rollback()
        db.close() 