import os
import pandas as pd
import requests
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DBManager:
    """
    Manages database operations for static data like brands, models, years, states, and versions.
    Also handles brand logo retrieval from a third-party repository.
    """
    
    def __init__(self, db_dir="db"):
        """
        Initialize the DBManager with the path to the database directory.
        
        Args:
            db_dir (str): Path to the database directory containing CSV files.
        """
        self.db_dir = db_dir
        self._ensure_db_dir_exists()
        self._load_data()
    
    def _ensure_db_dir_exists(self):
        """Ensure the database directory exists."""
        Path(self.db_dir).mkdir(parents=True, exist_ok=True)
    
    def _load_data(self):
        """Load all data from CSV files."""
        try:
            self.brands = self._load_csv("brands.csv")
            self.models = self._load_csv("models.csv")
            self.years = self._load_csv("years.csv")
            self.states = self._load_csv("states.csv")
            self.versions = self._load_csv("versions.csv")
            logger.info("All data loaded successfully")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            # Initialize empty DataFrames if files don't exist
            self.brands = pd.DataFrame(columns=["id", "name", "logo_url"])
            self.models = pd.DataFrame(columns=["id", "brand_id", "name"])
            self.years = pd.DataFrame(columns=["year"])
            self.states = pd.DataFrame(columns=["id", "name", "abbreviation"])
            self.versions = pd.DataFrame(columns=["id", "model_id", "name"])
    
    def _load_csv(self, filename):
        """
        Load data from a CSV file.
        
        Args:
            filename (str): Name of the CSV file.
            
        Returns:
            pandas.DataFrame: DataFrame containing the data from the CSV file.
        """
        file_path = os.path.join(self.db_dir, filename)
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            logger.warning(f"File {file_path} does not exist")
            return pd.DataFrame()
    
    def get_brands(self):
        """
        Get all brands.
        
        Returns:
            list: List of brand names.
        """
        return self.brands["name"].tolist() if not self.brands.empty else []
    
    def get_models_by_brand(self, brand_name):
        """
        Get all models for a specific brand.
        
        Args:
            brand_name (str): Name of the brand.
            
        Returns:
            list: List of model names for the specified brand.
        """
        if self.brands.empty or self.models.empty:
            return []
        
        brand_id = self.brands[self.brands["name"] == brand_name]["id"].iloc[0]
        return self.models[self.models["brand_id"] == brand_id]["name"].tolist()
    
    def get_years(self):
        """
        Get all available years.
        
        Returns:
            list: List of years.
        """
        return self.years["year"].tolist() if not self.years.empty else []
    
    def get_states(self):
        """
        Get all states.
        
        Returns:
            list: List of state names.
        """
        return self.states["name"].tolist() if not self.states.empty else []
    
    def get_versions_by_model(self, model_name):
        """
        Get all versions for a specific model.
        
        Args:
            model_name (str): Name of the model.
            
        Returns:
            list: List of version names for the specified model.
        """
        if self.models.empty or self.versions.empty:
            return []
        
        model_id = self.models[self.models["name"] == model_name]["id"].iloc[0]
        return self.versions[self.versions["model_id"] == model_id]["name"].tolist()
    
    def get_brand_logo_url(self, brand_name):
        """
        Get the logo URL for a specific brand.
        
        Args:
            brand_name (str): Name of the brand.
            
        Returns:
            str: URL of the brand logo.
        """
        if self.brands.empty:
            return None
        
        brand_row = self.brands[self.brands["name"] == brand_name]
        if brand_row.empty:
            return None
        
        return brand_row["logo_url"].iloc[0]
    
    def get_brand_logo(self, brand_name):
        """
        Get the logo for a specific brand.
        
        Args:
            brand_name (str): Name of the brand.
            
        Returns:
            bytes: Logo image data.
        """
        logo_url = self.get_brand_logo_url(brand_name)
        if not logo_url:
            return None
        
        try:
            response = requests.get(logo_url)
            if response.status_code == 200:
                return response.content
            else:
                logger.error(f"Failed to retrieve logo for {brand_name}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error retrieving logo for {brand_name}: {e}")
            return None
    
    def save_data(self):
        """Save all data to CSV files."""
        try:
            self._save_csv("brands.csv", self.brands)
            self._save_csv("models.csv", self.models)
            self._save_csv("years.csv", self.years)
            self._save_csv("states.csv", self.states)
            self._save_csv("versions.csv", self.versions)
            logger.info("All data saved successfully")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def _save_csv(self, filename, df):
        """
        Save data to a CSV file.
        
        Args:
            filename (str): Name of the CSV file.
            df (pandas.DataFrame): DataFrame containing the data to save.
        """
        file_path = os.path.join(self.db_dir, filename)
        df.to_csv(file_path, index=False)
        logger.info(f"Data saved to {file_path}")


# Create a singleton instance
db_manager = DBManager() 