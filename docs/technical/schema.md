sql
CREATE TABLE journal_entries (
id SERIAL PRIMARY KEY,
entry_date DATE NOT NULL,
day_of_week INTEGER NOT NULL,
content TEXT NOT NULL,
word_count INTEGER NOT NULL,
year INTEGER NOT NULL,
month INTEGER NOT NULL,
day INTEGER NOT NULL,
sentiment_score FLOAT,
complexity_score FLOAT,
topics JSONB,
mentioned_people JSONB,
mentioned_locations JSONB,
embedding vector(1536),
source_file VARCHAR NOT NULL,
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
updated_at TIMESTAMP WITH TIME ZONE
);