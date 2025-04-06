"""
Webmotors API client module.

This module provides a client for interacting with the Webmotors API.
"""

import base64
import json
import logging
import os
from typing import Any, Dict, List, Optional, Union

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class WebmotorsClient:
    """
    Client for interacting with the Webmotors API.
    
    This class handles authentication and provides methods for making API requests.
    """
    
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        api_username: Optional[str] = None,
        api_password: Optional[str] = None,
        base_url: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        """
        Initialize the Webmotors API client.
        
        Args:
            client_id: Webmotors API client ID
            client_secret: Webmotors API client secret
            api_username: Webmotors API username
            api_password: Webmotors API password
            base_url: Base URL for the Webmotors API
            api_version: API version to use
        """
        self.client_id = client_id or os.getenv("WEBMOTORS_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("WEBMOTORS_CLIENT_SECRET")
        self.api_username = api_username or os.getenv("WEBMOTORS_API_USERNAME")
        self.api_password = api_password or os.getenv("WEBMOTORS_API_PASSWORD")
        self.auth_base_url = "https://api-webmotors.sensedia.com/oauth/v1"
        self.base_url = base_url or os.getenv("WEBMOTORS_API_BASE_URL", "https://api-webmotors.sensedia.com")
        self.api_version = api_version or os.getenv("WEBMOTORS_API_VERSION", "v1")
        self.access_token = None
        
        # Log credentials (masked)
        logger.debug(f"Client ID: {self.client_id[:4]}...{self.client_id[-4:] if self.client_id else None}")
        logger.debug(f"Client Secret: {self.client_secret[:4]}...{self.client_secret[-4:] if self.client_secret else None}")
        logger.debug(f"API Username: {self.api_username[:4]}...{self.api_username[-4:] if self.api_username else None}")
        logger.debug(f"API Password: {'*' * 8 if self.api_password else None}")
        
        if not all([self.client_id, self.client_secret, self.api_username, self.api_password]):
            logger.warning(
                "Webmotors API credentials not found. Please set WEBMOTORS_CLIENT_ID, "
                "WEBMOTORS_CLIENT_SECRET, WEBMOTORS_API_USERNAME, and WEBMOTORS_API_PASSWORD "
                "environment variables."
            )
    
    def authenticate(self) -> bool:
        """
        Authenticate with the Webmotors API.
        
        Returns:
            True if authentication was successful, False otherwise
        """
        if not all([self.client_id, self.client_secret, self.api_username, self.api_password]):
            logger.error("Cannot authenticate: Missing required credentials")
            return False
        
        try:
            # Create authorization header with API credentials
            auth_string = f"{self.api_username}:{self.api_password}"
            auth_bytes = auth_string.encode("ascii")
            auth_b64 = base64.b64encode(auth_bytes).decode("ascii")
            
            # Make authentication request
            headers = {
                "Authorization": f"Basic {auth_b64}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            
            data = {
                "grant_type": "cliente",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
            
            url = f"{self.auth_base_url}/access-token"
            
            # Log complete request details
            logger.debug("Authentication request details:")
            logger.debug(f"URL: {url}")
            logger.debug(f"Headers: {headers}")
            logger.debug(f"Data: {data}")
            logger.debug(f"Base64 encoded auth: {auth_b64}")
            
            response = requests.post(
                url,
                headers=headers,
                data=data,
            )
            
            # Log response details
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            logger.debug(f"Response body: {response.text}")
            
            # Check response
            if response.status_code == 200:
                response_data = response.json()
                self.access_token = response_data.get("access_token")
                logger.info("Successfully authenticated with Webmotors API")
                return True
            else:
                logger.error(f"Authentication failed with status code {response.status_code}: {response.text}")
                logger.error(f"Response headers: {response.headers}")
                return False
                
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get headers for API requests.
        
        Returns:
            Dictionary of headers
        """
        if not self.access_token:
            self.authenticate()
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Make a request to the Webmotors API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            
        Returns:
            Response data as a dictionary, or None if the request failed
        """
        url = f"{self.base_url}/{endpoint}"
        logger.debug(f"Making {method} request to {url}")
        logger.debug(f"Headers: {self._get_headers()}")
        if params:
            logger.debug(f"Params: {params}")
        if data:
            logger.debug(f"Data: {data}")
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                params=params,
                json=data,
            )
            
            # Check if authentication failed
            if response.status_code == 401:
                logger.warning("Authentication token expired, attempting to re-authenticate")
                self.authenticate()
                
                # Retry the request
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self._get_headers(),
                    params=params,
                    json=data,
                )
            
            # Check response
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API request failed with status code {response.status_code}: {response.text}")
                logger.error(f"Response headers: {response.headers}")
                return None
                
        except Exception as e:
            logger.error(f"Error making API request: {e}")
            return None
    
    def get_catalog(self, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get catalog data from the Webmotors API.
        
        Args:
            params: Query parameters for the catalog request
            
        Returns:
            Catalog data as a dictionary, or None if the request failed
        """
        return self._make_request("GET", "catalog", params=params)
    
    def get_vehicle_details(self, vehicle_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific vehicle.
        
        Args:
            vehicle_id: ID of the vehicle
            
        Returns:
            Vehicle details as a dictionary, or None if the request failed
        """
        return self._make_request("GET", f"catalog/vehicle/{vehicle_id}")
    
    def get_financing_simulation(
        self,
        vehicle_id: str,
        down_payment: float,
        term_months: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Get financing simulation for a vehicle.
        
        Args:
            vehicle_id: ID of the vehicle
            down_payment: Down payment amount
            term_months: Term in months
            
        Returns:
            Financing simulation data as a dictionary, or None if the request failed
        """
        data = {
            "vehicleId": vehicle_id,
            "downPayment": down_payment,
            "termMonths": term_months,
        }
        
        return self._make_request("POST", "financing/simulation", data=data) 