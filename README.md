# Car Price Insights Dashboard

A data-driven dashboard for analyzing vehicle prices and identifying potential deals in the Brazilian market.

## 🚀 Overview

This project collects and analyzes vehicle listings from web sources to identify potential deals ("good opportunities"). By employing data scraping, data cleaning, exploratory data analysis (EDA), and predictive modeling, we estimate fair market prices for vehicles and highlight listings that appear to be underpriced.

## 🎯 Features

- **Data Collection**: Automated gathering of vehicle listings from chosen platforms
- **Data Analysis**: Comprehensive EDA and price prediction modeling
- **Interactive Dashboard**: Streamlit-based interface for data exploration
- **Deal Scoring**: Algorithm to identify potential bargains
- **Filtering Options**: Multiple criteria for data filtering and analysis

## 🛠️ Tech Stack

- **Python**: Core programming language
- **Streamlit**: Dashboard framework
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning models
- **BeautifulSoup/Selenium**: Web scraping
- **SQLite/MySQL**: Data storage

## 📋 Prerequisites

- Python 3.8+
- pip or conda package manager
- Git

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/car-insights.git
cd car-insights
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example .env file
cp .env.example .env

# Edit the .env file with your credentials
# You'll need to register at https://portal-webmotors.sensedia.com/api-portal/
# to get your Webmotors API credentials
```

5. Run the dashboard:
```bash
streamlit run src/app.py
```

## 📁 Project Structure

```
car-insights/
├── src/
│   ├── data/           # Data collection and processing
│   ├── models/         # ML models and predictions
│   ├── dashboard/      # Streamlit dashboard components
│   ├── services/       # External API services
│   └── utils/          # Utility functions
├── data/               # Raw and processed data
├── notebooks/          # Jupyter notebooks for analysis
├── tests/              # Test files
├── sprints/            # Sprint documentation
├── docs/               # Project documentation
└── requirements.txt    # Project dependencies
```

## 📊 Dashboard Pages

1. **Home**: Project overview and quick stats
2. **Data Explorer**: Interactive data exploration
3. **Price Analysis**: Price trends and distributions
4. **Opportunities**: List of potential deals
5. **Model Insights**: ML model performance and insights

## 🔑 API Integration

This project integrates with the Webmotors API to collect vehicle data. To use this feature:

1. Register at the [Webmotors API Portal](https://portal-webmotors.sensedia.com/api-portal/)
2. Create an application to get your client ID and client secret
3. Add these credentials to your `.env` file

For more information about the Webmotors API, refer to the following documentation:
- [Authentication Guide](https://portal-webmotors.sensedia.com/api-portal/documentacao/autenticacao)
- [Error Codes](https://portal-webmotors.sensedia.com/api-portal/documentacao/codigos-de-erro)
- [Catalog API](https://portal-webmotors.sensedia.com/api-portal/swagger/webmotors-catalogo-api/1.0.0)
- [Financing API](https://portal-webmotors.sensedia.com/api-portal/swagger/santander-financing-service-simulation/1.0)

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For any questions or suggestions, please open an issue in the GitHub repository. 