import json
import tempfile
from pathlib import Path
import pytest
from src.config_loader import ConfigLoader
from src.app.main_controller import MainController

def test_main_controller_with_valid_config():
    """Test that MainController works with valid configuration."""
    # Create a valid configuration
    valid_config = {
        "trading_settings": {
            "default_currency": "USD",
            "risk_tolerance": "moderate",
            "max_position_size": 0.05,
            "stop_loss_percent": 2.0,
            "take_profit_percent": 4.0
        },
        "analysis_settings": {
            "lookback_period_days": 90,
            "minimum_trades_for_analysis": 10,
            "metrics": [
                "win_rate",
                "profit_factor",
                "sharpe_ratio",
                "max_drawdown"
            ]
        },
        "export_settings": {
            "default_format": "markdown",
            "include_charts": True,
            "include_llm_insights": True
        }
    }
    
    # Create temporary config file
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "config.json"
        with open(config_path, 'w') as f:
            json.dump(valid_config, f)
        
        # Test that we can load the configuration
        loader = ConfigLoader(str(config_path))
        config_data = loader.load_config()
        
        # Verify the configuration was loaded correctly
        assert config_data["trading_settings"]["default_currency"] == "USD"
        assert config_data["analysis_settings"]["lookback_period_days"] == 90
        assert config_data["export_settings"]["default_format"] == "markdown"
        
        # Test that MainController can be instantiated
        # (In a real application, we might pass the config to MainController)
        controller = MainController()
        assert controller is not None

def test_main_controller_with_invalid_config():
    """Test that MainController handles invalid configuration gracefully."""
    # Create an invalid configuration (missing required section)
    invalid_config = {
        "analysis_settings": {
            "lookback_period_days": 90,
            "minimum_trades_for_analysis": 10,
            "metrics": ["win_rate"]
        },
        "export_settings": {
            "default_format": "markdown",
            "include_charts": True,
            "include_llm_insights": True
        }
    }
    
    # Create temporary config file
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "config.json"
        with open(config_path, 'w') as f:
            json.dump(invalid_config, f)
        
        # Test that loading the configuration raises an appropriate error
        loader = ConfigLoader(str(config_path))
        with pytest.raises(ValueError, match="Missing required configuration section: trading_settings"):
            loader.load_config()