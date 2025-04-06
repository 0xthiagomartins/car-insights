"""
Car validator module.

This module implements a validator for car data.
"""

import logging
from typing import Any, Dict, List, Tuple

# Configure logging
logger = logging.getLogger(__name__)


class CarValidator:
    """
    Validator for car data.
    
    This class validates car data to ensure it meets the required format and constraints.
    """
    
    def __init__(self, required_fields: List[str] = None, constraints: Dict[str, Dict[str, Any]] = None):
        """
        Initialize the car validator.
        
        Args:
            required_fields: List of required fields
            constraints: Dictionary of field constraints
        """
        self.required_fields = required_fields or [
            "title",
            "price",
            "year",
            "mileage",
            "source",
            "url",
        ]
        
        self.constraints = constraints or {
            "price": {"min": 0, "max": 1000000},
            "year": {"min": 1900, "max": 2023},
            "mileage": {"min": 0, "max": 500000},
        }
    
    def validate(self, data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Validate car data.
        
        Args:
            data: List of car dictionaries
            
        Returns:
            Tuple containing valid data and invalid data
        """
        valid_data = []
        invalid_data = []
        
        for item in data:
            if self._validate_item(item):
                valid_data.append(item)
            else:
                invalid_data.append(item)
        
        logger.info(f"Validated {len(data)} items: {len(valid_data)} valid, {len(invalid_data)} invalid")
        return valid_data, invalid_data
    
    def _validate_item(self, item: Dict[str, Any]) -> bool:
        """
        Validate a single car item.
        
        Args:
            item: Car dictionary
            
        Returns:
            True if the item is valid, False otherwise
        """
        # Check for required fields
        for field in self.required_fields:
            if field not in item:
                logger.warning(f"Missing required field: {field}")
                return False
        
        # Check field constraints
        for field, constraints in self.constraints.items():
            if field in item:
                value = item[field]
                
                # Check minimum value
                if "min" in constraints and value < constraints["min"]:
                    logger.warning(f"Field {field} value {value} is below minimum {constraints['min']}")
                    return False
                
                # Check maximum value
                if "max" in constraints and value > constraints["max"]:
                    logger.warning(f"Field {field} value {value} is above maximum {constraints['max']}")
                    return False
        
        return True 