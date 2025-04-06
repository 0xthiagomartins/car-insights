"""
Base collector module for data collection.

This module defines the base interface for all data collectors.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseCollector(ABC):
    """
    Base class for all data collectors.
    
    This abstract class defines the interface that all data collectors must implement.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the collector.
        
        Args:
            name: The name of the collector
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
    
    @abstractmethod
    def collect(self) -> List[Dict[str, Any]]:
        """
        Collect data from the source.
        
        Returns:
            A list of dictionaries containing the collected data
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate the collector configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        pass
    
    def __str__(self) -> str:
        """Return a string representation of the collector."""
        return f"{self.__class__.__name__}(name='{self.name}')" 