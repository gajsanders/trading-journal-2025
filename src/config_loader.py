import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigLoader:
    """
    Loads and validates application configuration from JSON files.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the ConfigLoader.
        
        Args:
            config_path: Path to the configuration file. If None, uses default path.
        """
        if config_path is None:
            # Use default path relative to workspace root
            workspace_root = os.getenv("WORKSPACE_ROOT", "")
            if not workspace_root:
                self.config_path = Path("data/config.json")
            else:
                self.config_path = Path(workspace_root) / "data" / "config.json"
        else:
            self.config_path = Path(config_path)
        
        self._config_data: Optional[Dict[str, Any]] = None
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load and validate configuration from JSON file.
        
        Returns:
            Dict containing the configuration data.
            
        Raises:
            FileNotFoundError: If the config file doesn't exist.
            json.JSONDecodeError: If the config file is not valid JSON.
            ValueError: If the config file is missing required keys or has invalid values.
        """
        if self._config_data is not None:
            return self._config_data
            
        # Check if file exists
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
        # Load JSON
        try:
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in configuration file: {e.msg}", e.doc, e.pos)
            
        # Validate configuration
        self._validate_config(config_data)
        
        self._config_data = config_data
        return config_data
    
    def _validate_config(self, config_data: Dict[str, Any]) -> None:
        """
        Validate the configuration data structure and values.
        
        Args:
            config_data: The configuration data to validate.
            
        Raises:
            ValueError: If validation fails.
        """
        # Check required top-level keys
        required_keys = ["trading_settings", "analysis_settings", "export_settings"]
        for key in required_keys:
            if key not in config_data:
                raise ValueError(f"Missing required configuration section: {key}")
        
        # Validate trading settings
        trading_settings = config_data.get("trading_settings", {})
        self._validate_trading_settings(trading_settings)
        
        # Validate analysis settings
        analysis_settings = config_data.get("analysis_settings", {})
        self._validate_analysis_settings(analysis_settings)
        
        # Validate export settings
        export_settings = config_data.get("export_settings", {})
        self._validate_export_settings(export_settings)
    
    def _validate_trading_settings(self, trading_settings: Dict[str, Any]) -> None:
        """Validate trading settings section."""
        if not isinstance(trading_settings, dict):
            raise ValueError("trading_settings must be a dictionary")
            
        # Validate required keys
        required_keys = ["default_currency", "risk_tolerance", "max_position_size", 
                        "stop_loss_percent", "take_profit_percent"]
        for key in required_keys:
            if key not in trading_settings:
                raise ValueError(f"Missing required trading setting: {key}")
        
        # Validate types and values
        if not isinstance(trading_settings["default_currency"], str):
            raise ValueError("default_currency must be a string")
            
        if not isinstance(trading_settings["risk_tolerance"], str):
            raise ValueError("risk_tolerance must be a string")
            
        if trading_settings["risk_tolerance"] not in ["conservative", "moderate", "aggressive"]:
            raise ValueError("risk_tolerance must be one of: conservative, moderate, aggressive")
            
        if not isinstance(trading_settings["max_position_size"], (int, float)):
            raise ValueError("max_position_size must be a number")
            
        if trading_settings["max_position_size"] <= 0 or trading_settings["max_position_size"] > 1:
            raise ValueError("max_position_size must be between 0 and 1")
            
        if not isinstance(trading_settings["stop_loss_percent"], (int, float)):
            raise ValueError("stop_loss_percent must be a number")
            
        if trading_settings["stop_loss_percent"] <= 0:
            raise ValueError("stop_loss_percent must be greater than 0")
            
        if not isinstance(trading_settings["take_profit_percent"], (int, float)):
            raise ValueError("take_profit_percent must be a number")
            
        if trading_settings["take_profit_percent"] <= 0:
            raise ValueError("take_profit_percent must be greater than 0")
    
    def _validate_analysis_settings(self, analysis_settings: Dict[str, Any]) -> None:
        """Validate analysis settings section."""
        if not isinstance(analysis_settings, dict):
            raise ValueError("analysis_settings must be a dictionary")
            
        # Validate required keys
        required_keys = ["lookback_period_days", "minimum_trades_for_analysis", "metrics"]
        for key in required_keys:
            if key not in analysis_settings:
                raise ValueError(f"Missing required analysis setting: {key}")
        
        # Validate types and values
        if not isinstance(analysis_settings["lookback_period_days"], int):
            raise ValueError("lookback_period_days must be an integer")
            
        if analysis_settings["lookback_period_days"] <= 0:
            raise ValueError("lookback_period_days must be greater than 0")
            
        if not isinstance(analysis_settings["minimum_trades_for_analysis"], int):
            raise ValueError("minimum_trades_for_analysis must be an integer")
            
        if analysis_settings["minimum_trades_for_analysis"] <= 0:
            raise ValueError("minimum_trades_for_analysis must be greater than 0")
            
        if not isinstance(analysis_settings["metrics"], list):
            raise ValueError("metrics must be a list")
            
        if len(analysis_settings["metrics"]) == 0:
            raise ValueError("metrics list cannot be empty")
            
        valid_metrics = ["win_rate", "profit_factor", "sharpe_ratio", "max_drawdown"]
        for metric in analysis_settings["metrics"]:
            if metric not in valid_metrics:
                raise ValueError(f"Invalid metric '{metric}'. Valid metrics are: {valid_metrics}")
    
    def _validate_export_settings(self, export_settings: Dict[str, Any]) -> None:
        """Validate export settings section."""
        if not isinstance(export_settings, dict):
            raise ValueError("export_settings must be a dictionary")
            
        # Validate required keys
        required_keys = ["default_format", "include_charts", "include_llm_insights"]
        for key in required_keys:
            if key not in export_settings:
                raise ValueError(f"Missing required export setting: {key}")
        
        # Validate types and values
        if not isinstance(export_settings["default_format"], str):
            raise ValueError("default_format must be a string")
            
        if export_settings["default_format"] not in ["markdown", "html", "pdf"]:
            raise ValueError("default_format must be one of: markdown, html, pdf")
            
        if not isinstance(export_settings["include_charts"], bool):
            raise ValueError("include_charts must be a boolean")
            
        if not isinstance(export_settings["include_llm_insights"], bool):
            raise ValueError("include_llm_insights must be a boolean")
    
    def get_trading_settings(self) -> Dict[str, Any]:
        """Get trading settings from configuration."""
        config = self.load_config()
        return config.get("trading_settings", {})
    
    def get_analysis_settings(self) -> Dict[str, Any]:
        """Get analysis settings from configuration."""
        config = self.load_config()
        return config.get("analysis_settings", {})
    
    def get_export_settings(self) -> Dict[str, Any]:
        """Get export settings from configuration."""
        config = self.load_config()
        return config.get("export_settings", {})