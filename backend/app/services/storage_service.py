from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
from ..models.journal import JournalEntry
from ..models.database import VectorEntry, StorageMetrics

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables and extensions"""
        with psycopg2.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                # Enable vector extension
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                
                # Create journal entries table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS journal_entries (
                        id BIGSERIAL PRIMARY KEY,
                        date DATE NOT NULL,
                        content TEXT NOT NULL,
                        word_count INTEGER NOT NULL,
                        year INTEGER NOT NULL,
                        month INTEGER NOT NULL,
                        day INTEGER NOT NULL,
                        metadata JSONB DEFAULT '{}'::jsonb,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create vectors table with pgvector
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS entry_vectors (
                        id BIGSERIAL PRIMARY KEY,
                        entry_id BIGINT REFERENCES journal_entries(id) ON DELETE CASCADE,
                        embedding vector(1536),
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes
                cur.execute("CREATE INDEX IF NOT EXISTS idx_entries_date ON journal_entries(date)")
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_vector_hnsw ON entry_vectors 
                    USING hnsw (embedding vector_cosine_ops)
                    WITH (m = 16, ef_construction = 64)
                """)
                
                conn.commit()
    
    def store_entries(self, entries: List[JournalEntry]) -> Dict[str, Any]:
        """Store journal entries and their vector embeddings"""
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    # Store journal entries
                    entry_data = [(
                        e.date.date(),
                        e.content,
                        e.word_count,
                        e.year,
                        e.month,
                        e.day,
                        e.metadata
                    ) for e in entries]
                    
                    query = """
                        INSERT INTO journal_entries 
                        (date, content, word_count, year, month, day, metadata)
                        VALUES %s
                        RETURNING id
                    """
                    
                    entry_ids = execute_values(
                        cur, 
                        query, 
                        entry_data,
                        fetch=True
                    )
                    
                    # Store vector embeddings if present
                    vector_data = []
                    for entry_id, entry in zip(entry_ids, entries):
                        if 'embedding' in entry.metadata:
                            vector_data.append((
                                entry_id[0],
                                entry.metadata['embedding']
                            ))
                    
                    if vector_data:
                        vector_query = """
                            INSERT INTO entry_vectors (entry_id, embedding)
                            VALUES %s
                        """
                        execute_values(cur, vector_query, vector_data)
                    
                    conn.commit()
                    
                    return {
                        "stored_entries": len(entries),
                        "stored_vectors": len(vector_data)
                    }
                    
        except Exception as e:
            logger.error(f"Error storing entries: {str(e)}", exc_info=True)
            raise
    
    def get_storage_metrics(self) -> StorageMetrics:
        """Get storage metrics"""
        with psycopg2.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                # Get table sizes
                cur.execute("""
                    SELECT 
                        pg_size_pretty(pg_total_relation_size('journal_entries')) as entries_size,
                        pg_size_pretty(pg_total_relation_size('entry_vectors')) as vectors_size,
                        (SELECT COUNT(*) FROM journal_entries) as total_entries,
                        (SELECT COUNT(*) FROM entry_vectors) as total_vectors,
                        (SELECT AVG(vector_dims(embedding)) FROM entry_vectors) as avg_dims
                """)
                
                result = cur.fetchone()
                
                return StorageMetrics(
                    total_entries=result[2],
                    total_vectors=result[3],
                    avg_vector_size=result[4] or 0,
                    storage_size=result[0],
                    index_size=result[1]
                )
    
    def optimize_storage(self):
        """Optimize database storage"""
        with psycopg2.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                # Vacuum analyze tables
                cur.execute("VACUUM ANALYZE journal_entries")
                cur.execute("VACUUM ANALYZE entry_vectors")
                
                # Reindex to optimize HNSW index
                cur.execute("REINDEX INDEX CONCURRENTLY idx_vector_hnsw")
                
                conn.commit() 