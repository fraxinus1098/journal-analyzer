import requests
import time
from typing import List, Dict

def monitor_uploads(task_ids: List[str], base_url: str = "https://your-repl-name.your-username.repl.co"):
    """Monitor the processing of uploaded files"""
    completed = set()
    
    while len(completed) < len(task_ids):
        for task_id in task_ids:
            if task_id in completed:
                continue
                
            response = requests.get(f"{base_url}/api/upload/status/{task_id}")
            status = response.json()
            
            if status["status"] == "completed":
                print(f"\nTask {task_id} completed!")
                print(f"Processed {status.get('entries_processed', 0)} entries")
                completed.add(task_id)
                
            elif status["status"] == "error":
                print(f"\nError in task {task_id}:")
                print(status.get("error", "Unknown error"))
                completed.add(task_id)
                
            else:
                print(f"\rProcessing {task_id}: {status.get('progress', 0):.1f}%", end="")
                
        time.sleep(1)  # Wait before next check
        
    # Get final storage metrics
    response = requests.get(f"{base_url}/api/storage/metrics")
    metrics = response.json()
    
    print("\n\nProcessing Complete!")
    print(f"Total entries stored: {metrics['total_entries']}")
    print(f"Total vectors stored: {metrics['total_vectors']}")
    print(f"Storage size: {metrics['storage_size']}")

# Example usage:
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python monitor_processing.py <task_id1> [task_id2 ...]")
        sys.exit(1)
        
    monitor_uploads(sys.argv[1:]) 