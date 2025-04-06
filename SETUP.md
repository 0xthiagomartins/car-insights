# Car Insights Development Environment Setup Guide

This guide will help you set up your development environment for the Car Insights project.

## Prerequisites

- Python 3.8 or higher
- Git
- A code editor (VS Code recommended)
- Windows, macOS, or Linux operating system

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/car-insights.git
cd car-insights
```

## Step 2: Set Up Virtual Environment

### Windows

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\activate
```

### macOS/Linux

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

## Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

## Step 4: Verify Installation

```bash
# Check if Streamlit is installed correctly
streamlit --version

# Run the application
streamlit run src/app.py
```

If everything is set up correctly, the application should open in your default web browser.

## Step 5: Jupyter Notebook Setup

To work with the Jupyter notebooks:

```bash
# Install Jupyter
pip install jupyter notebook

# Start Jupyter Notebook
jupyter notebook
```

This will open Jupyter Notebook in your default web browser, allowing you to work with the notebooks in the `/notebooks` directory.

## Troubleshooting

### Common Issues

1. **Virtual Environment Activation Fails**
   - Make sure you're in the project root directory
   - Try using the full path to the activation script

2. **Package Installation Errors**
   - Update pip: `python -m pip install --upgrade pip`
   - Try installing packages one by one to identify problematic dependencies

3. **Streamlit Not Found**
   - Ensure the virtual environment is activated
   - Try reinstalling Streamlit: `pip install streamlit`

### Getting Help

If you encounter any issues not covered in this guide, please:

1. Check the project documentation
2. Search for similar issues in the project repository
3. Contact the project maintainers

## Development Workflow

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Run tests to ensure everything works
4. Submit a pull request

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics) 