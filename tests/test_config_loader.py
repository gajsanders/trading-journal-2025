import json
import os
import tempfile
from pathlib import Path
import pytest
from src.config_loader import ConfigLoader

# Valid configuration for testing
VALID_TRADING_SETTINGS = {
    "default_currency": "USD",
    "risk_tolerance": "moderate",
    "max_position_size": 0.05,
    "stop_loss_percent": 2.0,
    "take_profit_percent": 4.0
}

VALID_ANALYSIS_SETTINGS = {
    "lookback_period_days": 90,
    "minimum_trades_for_analysis": 10,
    "metrics": [
        "win_rate",
        "profit_factor",
        "sharpe_ratio",
        "max_drawdown"
    ]
}

VALID_EXPORT_SETTINGS = {
    "default_format": "markdown",
    "include_charts": True,
    "include_llm_insights": True
}

def create_valid_config():
    """Helper function to create a valid configuration."""
    return {
        "trading_settings": VALID_TRADING_SETTINGS.copy(),
        "analysis_settings": VALID_ANALYSIS_SETTINGS.copy(),
        "export_settings": VALID_EXPORT_SETTINGS.copy()
    }

def create_temp_config(config_data):
    """Helper function to create a temporary config file."""
    tmp_dir = tempfile.TemporaryDirectory()
    config_path = Path(tmp_dir.name) / "config.json"
    with open(config_path, 'w') as f:
        json.dump(config_data, f)
    return tmp_dir, config_path

def test_config_loader_with_valid_config():
    """Test that ConfigLoader works correctly with valid configuration."""
    config_data = create_valid_config()
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        config_data = loader.load_config()
        
        assert config_data["trading_settings"] == VALID_TRADING_SETTINGS
        assert config_data["analysis_settings"] == VALID_ANALYSIS_SETTINGS
        assert config_data["export_settings"] == VALID_EXPORT_SETTINGS
        assert loader.get_trading_settings() == VALID_TRADING_SETTINGS
        assert loader.get_analysis_settings() == VALID_ANALYSIS_SETTINGS
        assert loader.get_export_settings() == VALID_EXPORT_SETTINGS
    finally:
        tmp_dir.cleanup()

def test_config_loader_file_not_found():
    """Test that ConfigLoader raises appropriate error for missing file."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "nonexistent.json"
        loader = ConfigLoader(str(config_path))
        
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            loader.load_config()

def test_config_loader_invalid_json():
    """Test that ConfigLoader raises appropriate error for invalid JSON."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "config.json"
        with open(config_path, 'w') as f:
            f.write("{ invalid json }")
        
        loader = ConfigLoader(str(config_path))
        
        with pytest.raises(json.JSONDecodeError):
            loader.load_config()

def test_config_loader_missing_top_level_keys():
    """Test that ConfigLoader validates required top-level keys."""
    # Missing trading_settings
    config_data = {
        "analysis_settings": VALID_ANALYSIS_SETTINGS,
        "export_settings": VALID_EXPORT_SETTINGS
    }
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="Missing required configuration section: trading_settings"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()
    
    # Missing analysis_settings
    config_data = {
        "trading_settings": VALID_TRADING_SETTINGS,
        "export_settings": VALID_EXPORT_SETTINGS
    }
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="Missing required configuration section: analysis_settings"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()
    
    # Missing export_settings
    config_data = {
        "trading_settings": VALID_TRADING_SETTINGS,
        "analysis_settings": VALID_ANALYSIS_SETTINGS
    }
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="Missing required configuration section: export_settings"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_trading_settings_type():
    """Test that ConfigLoader validates trading settings type."""
    config_data = create_valid_config()
    config_data["trading_settings"] = "not a dict"
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="trading_settings must be a dictionary"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_missing_trading_setting():
    """Test that ConfigLoader validates required trading settings keys."""
    config_data = create_valid_config()
    del config_data["trading_settings"]["default_currency"]
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="Missing required trading setting: default_currency"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_default_currency_type():
    """Test that ConfigLoader validates default_currency type."""
    config_data = create_valid_config()
    config_data["trading_settings"]["default_currency"] = 123
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="default_currency must be a string"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_risk_tolerance():
    """Test that ConfigLoader validates risk_tolerance value."""
    config_data = create_valid_config()
    config_data["trading_settings"]["risk_tolerance"] = "invalid"
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="risk_tolerance must be one of"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_max_position_size():
    """Test that ConfigLoader validates max_position_size value."""
    # Test too high
    config_data = create_valid_config()
    config_data["trading_settings"]["max_position_size"] = 1.5
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="max_position_size must be between 0 and 1"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()
    
    # Test negative
    config_data = create_valid_config()
    config_data["trading_settings"]["max_position_size"] = -0.1
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="max_position_size must be between 0 and 1"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_stop_loss_percent():
    """Test that ConfigLoader validates stop_loss_percent value."""
    config_data = create_valid_config()
    config_data["trading_settings"]["stop_loss_percent"] = 0
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="stop_loss_percent must be greater than 0"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_analysis_settings_type():
    """Test that ConfigLoader validates analysis settings type."""
    config_data = create_valid_config()
    config_data["analysis_settings"] = "not a dict"
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="analysis_settings must be a dictionary"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_missing_analysis_setting():
    """Test that ConfigLoader validates required analysis settings keys."""
    config_data = create_valid_config()
    del config_data["analysis_settings"]["lookback_period_days"]
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="Missing required analysis setting: lookback_period_days"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_lookback_period_days_type():
    """Test that ConfigLoader validates lookback_period_days type."""
    config_data = create_valid_config()
    config_data["analysis_settings"]["lookback_period_days"] = "not an int"
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="lookback_period_days must be an integer"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_metrics_type():
    """Test that ConfigLoader validates metrics type."""
    config_data = create_valid_config()
    config_data["analysis_settings"]["metrics"] = "not a list"
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="metrics must be a list"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_empty_metrics_list():
    """Test that ConfigLoader validates empty metrics list."""
    config_data = create_valid_config()
    config_data["analysis_settings"]["metrics"] = []
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="metrics list cannot be empty"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_metric():
    """Test that ConfigLoader validates metric values."""
    config_data = create_valid_config()
    config_data["analysis_settings"]["metrics"] = ["win_rate", "invalid_metric"]
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="Invalid metric 'invalid_metric'"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_export_settings_type():
    """Test that ConfigLoader validates export settings type."""
    config_data = create_valid_config()
    config_data["export_settings"] = "not a dict"
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="export_settings must be a dictionary"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_missing_export_setting():
    """Test that ConfigLoader validates required export settings keys."""
    config_data = create_valid_config()
    del config_data["export_settings"]["default_format"]
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="Missing required export setting: default_format"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_default_format():
    """Test that ConfigLoader validates default_format value."""
    config_data = create_valid_config()
    config_data["export_settings"]["default_format"] = "invalid_format"
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="default_format must be one of"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_invalid_include_charts_type():
    """Test that ConfigLoader validates include_charts type."""
    config_data = create_valid_config()
    config_data["export_settings"]["include_charts"] = "not a bool"
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="include_charts must be a boolean"):
            loader.load_config()
    finally:
        tmp_dir.cleanup()

def test_config_loader_caching():
    """Test that ConfigLoader caches configuration data."""
    config_data = create_valid_config()
    tmp_dir, config_path = create_temp_config(config_data)
    
    try:
        loader = ConfigLoader(str(config_path))
        
        # Load config first time
        config1 = loader.load_config()
        
        # Modify file to simulate change
        modified_config = create_valid_config()
        modified_config["trading_settings"]["default_currency"] = "EUR"
        with open(config_path, 'w') as f:
            json.dump(modified_config, f)
        
        # Load config second time - should return cached version
        config2 = loader.load_config()
        
        # Should be the same (cached)
        assert config1 == config2
        assert config1["trading_settings"]["default_currency"] == "USD"
        
        # Create new loader to force reload
        new_loader = ConfigLoader(str(config_path))
        config3 = new_loader.load_config()
        
        # Should be different (newly loaded)
        assert config3["trading_settings"]["default_currency"] == "EUR"
    finally:
        tmp_dir.cleanup()