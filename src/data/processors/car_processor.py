"""
Car processor module.

This module implements a processor for car data.
"""

import logging
import re
from typing import Any, Dict, List, Optional

# Configure logging
logger = logging.getLogger(__name__)


class CarProcessor:
    """
    Processor for car data.
    
    This class processes car data to clean and transform it.
    """
    
    def __init__(self):
        """Initialize the car processor."""
        # Regular expressions for extracting information from titles
        self.year_pattern = re.compile(r'\b(19|20)\d{2}\b')
        self.brand_model_pattern = re.compile(r'^([A-Za-z]+)\s+(.+)$')
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process car data.
        
        Args:
            data: List of car dictionaries
            
        Returns:
            Processed car data
        """
        processed_data = []
        
        for item in data:
            try:
                processed_item = self._process_item(item)
                processed_data.append(processed_item)
            except Exception as e:
                logger.error(f"Error processing item: {e}")
        
        logger.info(f"Processed {len(data)} items")
        return processed_data
    
    def _process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single car item.
        
        Args:
            item: Car dictionary
            
        Returns:
            Processed car dictionary
        """
        # Create a copy of the item to avoid modifying the original
        processed_item = item.copy()
        
        # Extract year from title if not present
        if "year" not in processed_item or not processed_item["year"]:
            year_match = self.year_pattern.search(processed_item["title"])
            if year_match:
                processed_item["year"] = int(year_match.group(0))
        
        # Extract brand and model from title
        brand_model_match = self.brand_model_pattern.match(processed_item["title"])
        if brand_model_match:
            processed_item["brand"] = brand_model_match.group(1)
            processed_item["model"] = brand_model_match.group(2)
        
        # Calculate price per mile
        if "price" in processed_item and "mileage" in processed_item and processed_item["mileage"] > 0:
            processed_item["price_per_mile"] = processed_item["price"] / processed_item["mileage"]
        
        # Calculate age
        if "year" in processed_item:
            current_year = 2023  # This should be updated dynamically
            processed_item["age"] = current_year - processed_item["year"]
            
            # Calculate price per age
            if "price" in processed_item and processed_item["age"] > 0:
                processed_item["price_per_age"] = processed_item["price"] / processed_item["age"]
        
        return processed_item 