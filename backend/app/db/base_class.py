from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

# Create a metadata instance
metadata = MetaData()

# Create the Base class with the metadata
Base = declarative_base(metadata=metadata) 