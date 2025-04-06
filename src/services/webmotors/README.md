# Webmotors API Client

This module provides a client for interacting with the Webmotors API. It handles authentication and provides methods for making API requests to various endpoints.

## Authentication

The client uses OAuth 2.0 client credentials flow for authentication. You need to provide your client ID and client secret, either directly when initializing the client or by setting the following environment variables:

```
WEBMOTORS_CLIENT_ID=your_client_id
WEBMOTORS_CLIENT_SECRET=your_client_secret
```

## Environment Variables

The client supports the following environment variables:

### Required Variables
- `WEBMOTORS_CLIENT_ID`: Your Webmotors API client ID
- `WEBMOTORS_CLIENT_SECRET`: Your Webmotors API client secret

### Optional Variables
- `WEBMOTORS_API_BASE_URL`: Base URL for the Webmotors API (default: `https://api.webmotors.com.br`)
- `WEBMOTORS_API_VERSION`: API version to use (default: `v1`)
- `MAX_PAGES`: Maximum number of pages to collect (default: `3`)
- `COLLECTION_DELAY`: Delay between requests in seconds (default: `1.0`)

You can set these variables in a `.env` file in the root of your project. See the `.env.example` file for a template.

## Usage

### Initialize the Client

```python
from src.services.webmotors.client import WebmotorsClient

# Initialize with environment variables
client = WebmotorsClient()

# Or initialize with explicit credentials
client = WebmotorsClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
)
```

### Get Catalog Data

```python
# Get all catalog data
catalog = client.get_catalog()

# Get catalog data with filters
catalog = client.get_catalog({
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2020,
})
```

### Get Vehicle Details

```python
# Get details for a specific vehicle
vehicle_details = client.get_vehicle_details("vehicle_id")
```

### Get Financing Simulation

```python
# Get financing simulation for a vehicle
simulation = client.get_financing_simulation(
    vehicle_id="vehicle_id",
    down_payment=10000.0,
    term_months=36,
)
```

## Error Handling

The client includes error handling for common API errors:

- Authentication failures
- Token expiration (automatic re-authentication)
- Request failures

All errors are logged using the Python logging module.

## Testing

You can test if your environment variables are set up correctly by running:

```bash
python src/services/webmotors/check_env.py
```

You can also test the client functionality by running:

```bash
python src/services/webmotors/test_client.py
```

## API Documentation

For more information about the Webmotors API, refer to the following documentation:

- [Authentication Guide](https://portal-webmotors.sensedia.com/api-portal/documentacao/autenticacao)
- [Error Codes](https://portal-webmotors.sensedia.com/api-portal/documentacao/codigos-de-erro)
- [Catalog API](https://portal-webmotors.sensedia.com/api-portal/swagger/webmotors-catalogo-api/1.0.0)
- [Financing API](https://portal-webmotors.sensedia.com/api-portal/swagger/santander-financing-service-simulation/1.0) 