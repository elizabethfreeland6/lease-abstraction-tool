"""
History Manager Module
Handles storage and retrieval of previous lease extractions
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional

HISTORY_DIR = "history"
INDEX_FILE = os.path.join(HISTORY_DIR, "index.json")

def ensure_history_dir():
    """Create history directory if it doesn't exist"""
    os.makedirs(HISTORY_DIR, exist_ok=True)
    
    # Create index file if it doesn't exist
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'w') as f:
            json.dump({"extractions": []}, f)

def generate_extraction_id() -> str:
    """Generate unique ID for extraction"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def save_extraction(filename: str, data: Dict) -> str:
    """
    Save extraction to history
    
    Args:
        filename: Original PDF filename
        data: Extracted data dictionary
        
    Returns:
        Extraction ID
    """
    ensure_history_dir()
    
    # Generate unique ID
    extraction_id = generate_extraction_id()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create extraction record
    extraction = {
        "id": extraction_id,
        "timestamp": timestamp,
        "filename": filename,
        "data": data
    }
    
    # Save individual extraction file
    extraction_file = os.path.join(HISTORY_DIR, f"{extraction_id}.json")
    with open(extraction_file, 'w') as f:
        json.dump(extraction, f, indent=2)
    
    # Update index
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)
    
    # Add to index (summary only)
    index_entry = {
        "id": extraction_id,
        "timestamp": timestamp,
        "filename": filename,
        "property_address": data.get('property_address', ''),
        "tenant_name": data.get('tenant_name', ''),
        "lease_start_date": data.get('lease_start_date', '')
    }
    
    index["extractions"].insert(0, index_entry)  # Add to beginning (newest first)
    
    # Keep only last 100 extractions
    if len(index["extractions"]) > 100:
        # Delete old extraction files
        for old_entry in index["extractions"][100:]:
            old_file = os.path.join(HISTORY_DIR, f"{old_entry['id']}.json")
            if os.path.exists(old_file):
                os.remove(old_file)
        
        index["extractions"] = index["extractions"][:100]
    
    # Save updated index
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)
    
    return extraction_id

def load_extraction(extraction_id: str) -> Optional[Dict]:
    """
    Load extraction from history
    
    Args:
        extraction_id: Extraction ID
        
    Returns:
        Extraction data or None if not found
    """
    extraction_file = os.path.join(HISTORY_DIR, f"{extraction_id}.json")
    
    if not os.path.exists(extraction_file):
        return None
    
    with open(extraction_file, 'r') as f:
        return json.load(f)

def list_extractions(search_term: str = "") -> List[Dict]:
    """
    List all extractions with optional search
    
    Args:
        search_term: Optional search term to filter results
        
    Returns:
        List of extraction summaries
    """
    ensure_history_dir()
    
    if not os.path.exists(INDEX_FILE):
        return []
    
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)
    
    extractions = index.get("extractions", [])
    
    # Filter by search term if provided
    if search_term:
        search_lower = search_term.lower()
        extractions = [
            e for e in extractions
            if search_lower in e.get('filename', '').lower()
            or search_lower in e.get('property_address', '').lower()
            or search_lower in e.get('tenant_name', '').lower()
        ]
    
    return extractions

def delete_extraction(extraction_id: str) -> bool:
    """
    Delete extraction from history
    
    Args:
        extraction_id: Extraction ID
        
    Returns:
        True if deleted successfully
    """
    ensure_history_dir()
    
    # Delete extraction file
    extraction_file = os.path.join(HISTORY_DIR, f"{extraction_id}.json")
    if os.path.exists(extraction_file):
        os.remove(extraction_file)
    
    # Update index
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r') as f:
            index = json.load(f)
        
        index["extractions"] = [
            e for e in index["extractions"]
            if e["id"] != extraction_id
        ]
        
        with open(INDEX_FILE, 'w') as f:
            json.dump(index, f, indent=2)
    
    return True

def clear_all_history() -> bool:
    """
    Clear all history
    
    Returns:
        True if cleared successfully
    """
    ensure_history_dir()
    
    # Delete all extraction files
    for filename in os.listdir(HISTORY_DIR):
        if filename.endswith('.json') and filename != 'index.json':
            os.remove(os.path.join(HISTORY_DIR, filename))
    
    # Reset index
    with open(INDEX_FILE, 'w') as f:
        json.dump({"extractions": []}, f)
    
    return True

def get_extraction_count() -> int:
    """
    Get total number of saved extractions
    
    Returns:
        Number of extractions
    """
    ensure_history_dir()
    
    if not os.path.exists(INDEX_FILE):
        return 0
    
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)
    
    return len(index.get("extractions", []))
