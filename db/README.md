# Database Directory

This directory contains CSV files that store static data used by the Car Insights application. These files contain information that rarely changes, such as car brands, models, years, states, and versions.

## Files

- `brands.csv`: Contains car brands with their IDs, names, and logo URLs.
- `models.csv`: Contains car models with their IDs, brand IDs, and names.
- `years.csv`: Contains available years for vehicles.
- `states.csv`: Contains Brazilian states with their IDs, names, and abbreviations.
- `versions.csv`: Contains car versions with their IDs, model IDs, and names.

## Structure

### brands.csv
```
id,name,logo_url
1,Toyota,https://raw.githubusercontent.com/thiagomartins/car-logos/main/logos/toyota.png
2,Honda,https://raw.githubusercontent.com/thiagomartins/car-logos/main/logos/honda.png
...
```

### models.csv
```
id,brand_id,name
1,1,Corolla
2,1,Camry
...
```

### years.csv
```
year
2010
2011
...
```

### states.csv
```
id,name,abbreviation
1,Acre,AC
2,Alagoas,AL
...
```

### versions.csv
```
id,model_id,name
1,1,1.8
2,1,2.0
...
```

## Usage

These files are used by the `DBManager` class in `src/data/db_manager.py` to provide data for the application. The `DBManager` class provides methods to retrieve data from these files and to handle brand logo retrieval from a third-party repository.

## Brand Logos

Brand logos are stored in a third-party repository and accessed via URLs. The URLs are stored in the `brands.csv` file. The `DBManager` class provides methods to retrieve these logos.

## Updating Data

To update the data in these files, you can either:

1. Edit the CSV files directly.
2. Use the `DBManager` class to load the data, modify it, and save it back to the CSV files.

Example:
```python
from src.data import db_manager

# Load data
db_manager._load_data()

# Modify data
db_manager.brands = db_manager.brands.append({"id": 16, "name": "New Brand", "logo_url": "https://example.com/logo.png"})

# Save data
db_manager.save_data()
``` 