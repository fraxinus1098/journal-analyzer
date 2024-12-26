from sqlalchemy import text
from .models import JournalEntry
from typing import List

def create_vector_similarity_index(db):
    """Create an index for vector similarity search"""
    query = text("""
    CREATE INDEX IF NOT EXISTS journal_entries_embedding_idx 
    ON journal_entries 
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
    """)
    
    db.execute(query)
    db.commit()

def find_similar_entries(db, embedding: List[float], limit: int = 5):
    """Find similar journal entries based on vector similarity"""
    query = text("""
    SELECT id, content, embedding <=> :embedding AS distance
    FROM journal_entries
    ORDER BY embedding <=> :embedding
    LIMIT :limit
    """)
    
    result = db.execute(
        query,
        {"embedding": embedding, "limit": limit}
    )
    
    return result.fetchall()
