"""
Webmotors collector module.

This module implements a collector for the Webmotors API.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from src.services.webmotors.client import WebmotorsClient
from .base_collector import BaseCollector

# Configure logging
logger = logging.getLogger(__name__)


class WebmotorsCollector(BaseCollector):
    """
    Collector for Webmotors API.
    
    This collector retrieves car listings from the Webmotors API.
    """
    
    def __init__(
        self,
        name: str = "webmotors",
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the Webmotors collector.
        
        Args:
            name: The name of the collector
            config: Optional configuration dictionary
        """
        super().__init__(name, config)
        self.client = WebmotorsClient()
    
    def validate_config(self) -> bool:
        """
        Validate the collector configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        # Check if required configuration parameters are present
        required_params = ["max_pages", "filters"]
        for param in required_params:
            if param not in self.config:
                logger.error(f"Missing required configuration parameter: {param}")
                return False
        
        # Validate parameter values
        if not isinstance(self.config["max_pages"], int) or self.config["max_pages"] < 1:
            logger.error("max_pages must be a positive integer")
            return False
        
        if not isinstance(self.config["filters"], dict):
            logger.error("filters must be a dictionary")
            return False
        
        return True
    
    def collect(self) -> List[Dict[str, Any]]:
        """
        Collect car listings from Webmotors API.
        
        Returns:
            A list of dictionaries containing car listings
        """
        if not self.validate_config():
            logger.error("Invalid configuration")
            return []
        
        # Get configuration from environment variables if not provided
        max_pages = self.config.get("max_pages", int(os.getenv("MAX_PAGES", "3")))
        filters = self.config.get("filters", {})
        
        all_listings = []
        
        # Authenticate with the API
        if not self.client.authenticate():
            logger.error("Failed to authenticate with Webmotors API")
            return []
        
        for page in range(1, max_pages + 1):
            logger.info(f"Collecting page {page} of {max_pages}")
            
            # Add page to filters
            page_filters = filters.copy()
            page_filters["page"] = page
            
            try:
                # Get catalog data
                catalog = self.client.get_catalog(params=page_filters)
                
                if not catalog:
                    logger.warning(f"No data returned for page {page}")
                    continue
                
                # Extract vehicles from catalog
                vehicles = catalog.get("vehicles", [])
                
                # Process each vehicle
                for vehicle in vehicles:
                    try:
                        # Get vehicle details
                        vehicle_id = vehicle.get("id")
                        if vehicle_id:
                            vehicle_details = self.client.get_vehicle_details(vehicle_id)
                            
                            if vehicle_details:
                                # Create listing dictionary
                                listing = self._create_listing(vehicle, vehicle_details)
                                all_listings.append(listing)
                            else:
                                logger.warning(f"Failed to get details for vehicle {vehicle_id}")
                        else:
                            logger.warning("Vehicle ID not found in catalog data")
                            
                    except Exception as e:
                        logger.error(f"Error processing vehicle: {e}")
                
                logger.info(f"Collected {len(vehicles)} listings from page {page}")
                
                # Check if we've reached the last page
                if "pagination" in catalog and "totalPages" in catalog["pagination"]:
                    total_pages = catalog["pagination"]["totalPages"]
                    if page >= total_pages:
                        logger.info(f"Reached last page ({total_pages})")
                        break
                
            except Exception as e:
                logger.error(f"Error collecting page {page}: {e}")
        
        logger.info(f"Collected a total of {len(all_listings)} listings")
        return all_listings
    
    def _create_listing(self, vehicle: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a listing dictionary from vehicle and details data.
        
        Args:
            vehicle: Vehicle data from catalog
            details: Vehicle details data
            
        Returns:
            A dictionary containing the listing data
        """
        # Extract basic information
        listing = {
            "id": vehicle.get("id"),
            "title": vehicle.get("title", "Unknown"),
            "brand": vehicle.get("brand", "Unknown"),
            "model": vehicle.get("model", "Unknown"),
            "year": vehicle.get("year"),
            "price": vehicle.get("price"),
            "mileage": vehicle.get("mileage"),
            "source": "webmotors",
            "url": vehicle.get("url", ""),
        }
        
        # Add details if available
        if details:
            listing.update({
                "color": details.get("color"),
                "transmission": details.get("transmission"),
                "fuel": details.get("fuel"),
                "doors": details.get("doors"),
                "seats": details.get("seats"),
                "description": details.get("description"),
                "features": details.get("features", []),
                "images": details.get("images", []),
                "seller": details.get("seller", {}),
                "location": details.get("location", {}),
            })
        
        return listing 