"""
Data collection script.

This script collects, processes, and validates car data from various sources.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from data.collectors.cars_com_collector import CarsComCollector
from data.collectors.webmotors_collector import WebmotorsCollector
from data.processors.car_processor import CarProcessor
from data.validators.car_validator import CarValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def collect_data(
    output_dir: str = "data/raw",
    config: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Collect, process, and validate car data.
    
    Args:
        output_dir: Directory to save the collected data
        config: Configuration dictionary
        
    Returns:
        List of processed and validated car dictionaries
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize collectors
    collectors = [
        CarsComCollector(
            config={
                "max_pages": 3,
                "delay": 1.0,
            }
        ),
        WebmotorsCollector(
            config={
                "max_pages": 3,
                "filters": {
                    "brand": "Toyota",
                    "model": "Corolla",
                    "year": 2020,
                },
            }
        ),
        # Add more collectors here
    ]
    
    # Initialize processor and validator
    processor = CarProcessor()
    validator = CarValidator()
    
    # Collect data from all sources
    all_data = []
    
    for collector in collectors:
        logger.info(f"Collecting data from {collector.name}")
        
        try:
            # Collect data
            data = collector.collect()
            logger.info(f"Collected {len(data)} items from {collector.name}")
            
            # Process data
            processed_data = processor.process(data)
            logger.info(f"Processed {len(processed_data)} items from {collector.name}")
            
            # Validate data
            valid_data, invalid_data = validator.validate(processed_data)
            logger.info(f"Validated {len(processed_data)} items: {len(valid_data)} valid, {len(invalid_data)} invalid")
            
            # Add valid data to the collection
            all_data.extend(valid_data)
            
            # Save raw data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_filename = os.path.join(output_dir, f"{collector.name}_{timestamp}_raw.json")
            
            with open(raw_filename, "w") as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved raw data to {raw_filename}")
            
            # Save processed data
            processed_filename = os.path.join(output_dir, f"{collector.name}_{timestamp}_processed.json")
            
            with open(processed_filename, "w") as f:
                json.dump(processed_data, f, indent=2)
            
            logger.info(f"Saved processed data to {processed_filename}")
            
            # Save valid data
            valid_filename = os.path.join(output_dir, f"{collector.name}_{timestamp}_valid.json")
            
            with open(valid_filename, "w") as f:
                json.dump(valid_data, f, indent=2)
            
            logger.info(f"Saved valid data to {valid_filename}")
            
        except Exception as e:
            logger.error(f"Error collecting data from {collector.name}: {e}")
    
    # Save all collected data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    all_data_filename = os.path.join(output_dir, f"all_data_{timestamp}.json")
    
    with open(all_data_filename, "w") as f:
        json.dump(all_data, f, indent=2)
    
    logger.info(f"Saved all data to {all_data_filename}")
    
    return all_data


if __name__ == "__main__":
    # Collect data
    data = collect_data()
    
    # Print summary
    logger.info(f"Collected a total of {len(data)} valid car listings") 