"""
Cars.com collector module.

This module implements a collector for the cars.com website.
"""

import logging
import time
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from .base_collector import BaseCollector

# Configure logging
logger = logging.getLogger(__name__)


class CarsComCollector(BaseCollector):
    """
    Collector for cars.com website.
    
    This collector scrapes car listings from cars.com.
    """
    
    def __init__(
        self,
        name: str = "cars_com",
        base_url: str = "https://www.cars.com",
        search_path: str = "/shopping/results/",
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the Cars.com collector.
        
        Args:
            name: The name of the collector
            base_url: The base URL for the website
            search_path: The path for search results
            config: Optional configuration dictionary
        """
        super().__init__(name, config)
        self.base_url = base_url
        self.search_path = search_path
        self.session = requests.Session()
        
        # Set default headers to mimic a browser
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })
    
    def validate_config(self) -> bool:
        """
        Validate the collector configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        # Check if required configuration parameters are present
        required_params = ["max_pages", "delay"]
        for param in required_params:
            if param not in self.config:
                logger.error(f"Missing required configuration parameter: {param}")
                return False
        
        # Validate parameter values
        if not isinstance(self.config["max_pages"], int) or self.config["max_pages"] < 1:
            logger.error("max_pages must be a positive integer")
            return False
        
        if not isinstance(self.config["delay"], (int, float)) or self.config["delay"] < 0:
            logger.error("delay must be a non-negative number")
            return False
        
        return True
    
    def collect(self) -> List[Dict[str, Any]]:
        """
        Collect car listings from cars.com.
        
        Returns:
            A list of dictionaries containing car listings
        """
        if not self.validate_config():
            logger.error("Invalid configuration")
            return []
        
        all_listings = []
        max_pages = self.config.get("max_pages", 1)
        delay = self.config.get("delay", 1.0)
        
        for page in range(1, max_pages + 1):
            logger.info(f"Collecting page {page} of {max_pages}")
            
            # Construct the URL for the current page
            url = f"{self.base_url}{self.search_path}?page={page}"
            
            try:
                # Add a delay to avoid overloading the server
                time.sleep(delay)
                
                # Make the request
                response = self.session.get(url)
                response.raise_for_status()
                
                # Parse the HTML
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Extract car listings
                listings = self._extract_listings(soup)
                all_listings.extend(listings)
                
                logger.info(f"Collected {len(listings)} listings from page {page}")
                
            except requests.RequestException as e:
                logger.error(f"Error collecting page {page}: {e}")
            
            except Exception as e:
                logger.error(f"Unexpected error collecting page {page}: {e}")
        
        logger.info(f"Collected a total of {len(all_listings)} listings")
        return all_listings
    
    def _extract_listings(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract car listings from the HTML.
        
        Args:
            soup: BeautifulSoup object containing the HTML
            
        Returns:
            A list of dictionaries containing car listings
        """
        listings = []
        
        # This is a placeholder implementation
        # The actual selectors would need to be updated based on the website structure
        
        # Find all listing elements
        listing_elements = soup.select(".vehicle-card")
        
        for element in listing_elements:
            try:
                # Extract listing data
                title_element = element.select_one(".title")
                price_element = element.select_one(".price")
                year_element = element.select_one(".year")
                mileage_element = element.select_one(".mileage")
                
                # Create listing dictionary
                listing = {
                    "title": title_element.text.strip() if title_element else "Unknown",
                    "price": self._extract_price(price_element.text.strip() if price_element else "0"),
                    "year": int(year_element.text.strip()) if year_element else None,
                    "mileage": self._extract_mileage(mileage_element.text.strip() if mileage_element else "0"),
                    "source": "cars.com",
                    "url": self._extract_url(element),
                }
                
                listings.append(listing)
                
            except Exception as e:
                logger.error(f"Error extracting listing: {e}")
        
        return listings
    
    def _extract_price(self, price_text: str) -> float:
        """
        Extract price from text.
        
        Args:
            price_text: Text containing the price
            
        Returns:
            The extracted price as a float
        """
        # Remove non-numeric characters except decimal point
        numeric_text = "".join(c for c in price_text if c.isdigit() or c == ".")
        
        try:
            return float(numeric_text)
        except ValueError:
            return 0.0
    
    def _extract_mileage(self, mileage_text: str) -> int:
        """
        Extract mileage from text.
        
        Args:
            mileage_text: Text containing the mileage
            
        Returns:
            The extracted mileage as an integer
        """
        # Remove non-numeric characters
        numeric_text = "".join(c for c in mileage_text if c.isdigit())
        
        try:
            return int(numeric_text)
        except ValueError:
            return 0
    
    def _extract_url(self, element: BeautifulSoup) -> str:
        """
        Extract URL from listing element.
        
        Args:
            element: BeautifulSoup element containing the listing
            
        Returns:
            The extracted URL
        """
        link_element = element.select_one("a")
        
        if link_element and "href" in link_element.attrs:
            href = link_element["href"]
            if href.startswith("/"):
                return f"{self.base_url}{href}"
            return href
        
        return "" 