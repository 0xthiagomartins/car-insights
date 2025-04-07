import pytest
import pandas as pd
import os
from src.data.db_manager import DBManager

@pytest.fixture
def db_manager():
    """Create a DBManager instance for testing."""
    return DBManager(db_dir="tests/data/test_db")

def test_get_brands(db_manager):
    """Test getting all brands."""
    brands = db_manager.get_brands()
    assert isinstance(brands, list)
    assert len(brands) > 0
    assert "Toyota" in brands
    assert "Honda" in brands

def test_get_models_by_brand(db_manager):
    """Test getting models for a specific brand."""
    models = db_manager.get_models_by_brand("Toyota")
    assert isinstance(models, list)
    assert len(models) > 0
    assert "Corolla" in models
    assert "Camry" in models

def test_get_years(db_manager):
    """Test getting all years."""
    years = db_manager.get_years()
    assert isinstance(years, list)
    assert len(years) > 0
    assert 2020 in years
    assert 2021 in years
    assert 2022 in years

def test_get_states(db_manager):
    """Test getting all states."""
    states = db_manager.get_states()
    assert isinstance(states, list)
    assert len(states) > 0
    assert "São Paulo" in states
    assert "Rio de Janeiro" in states

def test_get_versions_by_model(db_manager):
    """Test getting versions for a specific model."""
    versions = db_manager.get_versions_by_model("Corolla")
    assert isinstance(versions, list)
    assert len(versions) > 0
    assert "1.8" in versions
    assert "2.0" in versions

def test_get_brand_logo_url(db_manager):
    """Test getting the logo URL for a specific brand."""
    logo_url = db_manager.get_brand_logo_url("Toyota")
    assert isinstance(logo_url, str)
    assert logo_url.startswith("http")
    assert "toyota" in logo_url.lower()

def test_get_brand_logo(db_manager):
    """Test getting the logo for a specific brand."""
    logo = db_manager.get_brand_logo("Toyota")
    assert logo is not None
    assert isinstance(logo, bytes)
    assert len(logo) > 0 