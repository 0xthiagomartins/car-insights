"""
Test script for the Webmotors API client.

This script tests the basic functionality of the Webmotors API client.
"""

import logging
import os
import sys
from typing import Dict, Any, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from src.services.webmotors.client import WebmotorsClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def test_authentication() -> bool:
    """
    Test authentication with the Webmotors API.
    
    Returns:
        True if authentication was successful, False otherwise
    """
    logger.info("Testing authentication...")
    
    client = WebmotorsClient()
    result = client.authenticate()
    
    if result:
        logger.info("Authentication successful")
    else:
        logger.error("Authentication failed")
    
    return result


def test_get_catalog() -> Optional[Dict[str, Any]]:
    """
    Test getting catalog data from the Webmotors API.
    
    Returns:
        Catalog data as a dictionary, or None if the request failed
    """
    logger.info("Testing get_catalog...")
    
    client = WebmotorsClient()
    
    # Authenticate first
    if not client.authenticate():
        logger.error("Authentication failed, cannot test get_catalog")
        return None
    
    # Get catalog data
    catalog = client.get_catalog()
    
    if catalog:
        logger.info(f"Successfully retrieved catalog data with {len(catalog.get('vehicles', []))} vehicles")
    else:
        logger.error("Failed to retrieve catalog data")
    
    return catalog


def test_get_vehicle_details(vehicle_id: str) -> Optional[Dict[str, Any]]:
    """
    Test getting vehicle details from the Webmotors API.
    
    Args:
        vehicle_id: ID of the vehicle
        
    Returns:
        Vehicle details as a dictionary, or None if the request failed
    """
    logger.info(f"Testing get_vehicle_details for vehicle {vehicle_id}...")
    
    client = WebmotorsClient()
    
    # Authenticate first
    if not client.authenticate():
        logger.error("Authentication failed, cannot test get_vehicle_details")
        return None
    
    # Get vehicle details
    details = client.get_vehicle_details(vehicle_id)
    
    if details:
        logger.info(f"Successfully retrieved details for vehicle {vehicle_id}")
    else:
        logger.error(f"Failed to retrieve details for vehicle {vehicle_id}")
    
    return details


def main() -> None:
    """
    Main function for testing the Webmotors API client.
    """
    # Test authentication
    if not test_authentication():
        logger.error("Authentication test failed, cannot proceed with other tests")
        return
    
    # Test get_catalog
    catalog = test_get_catalog()
    
    # If we have a catalog, test get_vehicle_details with the first vehicle
    if catalog and "vehicles" in catalog and catalog["vehicles"]:
        vehicle_id = catalog["vehicles"][0]["id"]
        test_get_vehicle_details(vehicle_id)
    else:
        logger.warning("No vehicles found in catalog, cannot test get_vehicle_details")


if __name__ == "__main__":
    main() 