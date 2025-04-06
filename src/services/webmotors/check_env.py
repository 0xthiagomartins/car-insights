"""
Environment variable checker for Webmotors API.

This script checks if the required environment variables for the Webmotors API are set up correctly.
"""

import os
import sys
from typing import Dict, List, Tuple

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_env_vars() -> Tuple[bool, List[str], List[str]]:
    """
    Check if the required environment variables are set up correctly.
    
    Returns:
        A tuple containing:
        - A boolean indicating if all required variables are set
        - A list of missing variables
        - A list of optional variables that are set
    """
    # Required environment variables
    required_vars = [
        "WEBMOTORS_CLIENT_ID",
        "WEBMOTORS_CLIENT_SECRET",
    ]
    
    # Optional environment variables
    optional_vars = [
        "WEBMOTORS_API_BASE_URL",
        "WEBMOTORS_API_VERSION",
        "MAX_PAGES",
        "COLLECTION_DELAY",
    ]
    
    # Check required variables
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    # Check optional variables
    set_optional_vars = []
    for var in optional_vars:
        if os.getenv(var):
            set_optional_vars.append(var)
    
    # Check if all required variables are set
    all_set = len(missing_vars) == 0
    
    return all_set, missing_vars, set_optional_vars


def main() -> None:
    """
    Main function for checking environment variables.
    """
    print("Checking environment variables for Webmotors API...")
    
    all_set, missing_vars, set_optional_vars = check_env_vars()
    
    if all_set:
        print("✅ All required environment variables are set.")
    else:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file.")
        print("You can copy the .env.example file and update it with your credentials.")
    
    if set_optional_vars:
        print("\n✅ Optional environment variables that are set:")
        for var in set_optional_vars:
            print(f"  - {var}")
    
    if all_set:
        print("\nYou can now use the Webmotors API client.")
        print("Try running the test script: python src/services/webmotors/test_client.py")
    else:
        print("\nPlease set up your environment variables before using the Webmotors API client.")


if __name__ == "__main__":
    main() 