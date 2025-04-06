"""
Example script demonstrating how to use the Webmotors API client.
"""

import json
import logging
import os
from typing import Dict, Any, Optional

from dotenv import load_dotenv
from client import WebmotorsClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def print_json(data: Optional[Dict[str, Any]], indent: int = 2) -> None:
    """
    Print JSON data in a formatted way.
    
    Args:
        data: JSON data to print
        indent: Indentation level
    """
    if data:
        print(json.dumps(data, indent=indent))
    else:
        print("No data returned")


def main() -> None:
    """
    Main function demonstrating the Webmotors API client.
    """
    # Initialize the client
    client = WebmotorsClient()
    
    # Authenticate
    if not client.authenticate():
        logger.error("Failed to authenticate with Webmotors API")
        return
    
    # Get catalog data
    logger.info("Getting catalog data...")
    catalog = client.get_catalog()
    print("\nCatalog Data:")
    print_json(catalog)
    
    # Get catalog data with filters
    logger.info("Getting filtered catalog data...")
    filtered_catalog = client.get_catalog({
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2020,
    })
    print("\nFiltered Catalog Data:")
    print_json(filtered_catalog)
    
    # If we have vehicle IDs from the catalog, get details for the first one
    if catalog and "vehicles" in catalog and catalog["vehicles"]:
        vehicle_id = catalog["vehicles"][0]["id"]
        
        # Get vehicle details
        logger.info(f"Getting details for vehicle {vehicle_id}...")
        vehicle_details = client.get_vehicle_details(vehicle_id)
        print(f"\nVehicle Details for {vehicle_id}:")
        print_json(vehicle_details)
        
        # Get financing simulation
        logger.info(f"Getting financing simulation for vehicle {vehicle_id}...")
        simulation = client.get_financing_simulation(
            vehicle_id=vehicle_id,
            down_payment=10000.0,
            term_months=36,
        )
        print(f"\nFinancing Simulation for {vehicle_id}:")
        print_json(simulation)


if __name__ == "__main__":
    main() 