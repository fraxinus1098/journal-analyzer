import requests
from datetime import datetime
from typing import Dict, Any

def verify_processing(base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """Verify that PDFs were processed correctly"""
    
    # Get storage metrics
    metrics = requests.get(f"{base_url}/api/storage/metrics").json()
    
    # Get year coverage
    coverage = requests.get(f"{base_url}/api/analysis/coverage").json()
    
    # Get basic statistics
    stats = requests.get(f"{base_url}/api/analysis/basic-stats").json()
    
    return {
        "storage_metrics": metrics,
        "year_coverage": coverage,
        "basic_stats": stats
    }

if __name__ == "__main__":
    results = verify_processing()
    
    print("\nProcessing Verification Results:")
    print("-" * 40)
    
    print("\nStorage Metrics:")
    print(f"Total Entries: {results['storage_metrics']['total_entries']}")
    print(f"Total Vectors: {results['storage_metrics']['total_vectors']}")
    print(f"Storage Size: {results['storage_metrics']['storage_size']}")
    
    print("\nYear Coverage:")
    for year, count in results['year_coverage'].items():
        print(f"{year}: {count} entries")
    
    print("\nBasic Statistics:")
    print(f"Average Words per Entry: {results['basic_stats']['avg_words_per_entry']:.1f}")
    print(f"Total Word Count: {results['basic_stats']['total_words']:,}") 