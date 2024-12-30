"""
Service for managing processing status.
"""
from typing import Dict, Optional
from datetime import datetime, timedelta

class StatusManager:
    _instances: Dict[int, 'ProcessingStatus'] = {}
    
    @classmethod
    def create(cls) -> 'ProcessingStatus':
        status = ProcessingStatus()
        cls._instances[id(status)] = status
        return status
    
    @classmethod
    def get(cls, status_id: int) -> Optional['ProcessingStatus']:
        # Clean up old statuses (older than 1 hour)
        current_time = datetime.utcnow()
        cls._instances = {
            k: v for k, v in cls._instances.items()
            if current_time - v.created_at < timedelta(hours=1)
        }
        return cls._instances.get(status_id)
    
    @classmethod
    def remove(cls, status_id: int) -> None:
        if status_id in cls._instances:
            del cls._instances[status_id]

class ProcessingStatus:
    def __init__(self):
        self.status = "processing"
        self.progress = 0
        self.errors = []
        self.success_count = 0
        self.created_at = datetime.utcnow() 