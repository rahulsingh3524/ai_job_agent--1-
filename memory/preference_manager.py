# memory/preference_manager.py

"""
Preference Manager
------------------
Handles persistent user preferences for job crawling, applications, and resume optimization.
"""

import json
import os

def load_preferences():
    """Load user preferences from JSON file."""
    default_prefs = {
        "roles": ["Software Engineer", "Developer"],
        "locations": ["India"],
        "followup_days": 5,
        "desired_count": 100,
        "easy_apply_only": True,
        "companies": ["Google", "Microsoft", "TCS", "Infosys", "Wipro"]  # Default companies
    }
    
    try:
        if os.path.exists("preferences.json"):
            with open("preferences.json", "r") as f:
                prefs = json.load(f)
                # Ensure all default keys exist
                for key, value in default_prefs.items():
                    if key not in prefs:
                        prefs[key] = value
                return prefs
    except Exception as e:
        print(f"Error loading preferences: {e}")
    
    return default_prefs

def save_preferences(preferences):
    """Save user preferences to JSON file."""
    try:
        with open("preferences.json", "w") as f:
            json.dump(preferences, f, indent=2)
    except Exception as e:
        print(f"Error saving preferences: {e}")

def update_preference(key, value):
    prefs = load_preferences()
    prefs[key] = value
    save_preferences(prefs)
