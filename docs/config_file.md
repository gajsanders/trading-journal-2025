# Configuration File Guide

## Overview

The Trading Journal application uses a JSON configuration file to control various aspects of its behavior. The configuration file is located at `data/config.json` relative to the workspace root.

## Configuration Structure

The configuration file has three main sections:

### trading_settings
Controls trading-related parameters:
- `default_currency`: The currency used for all trades (string, e.g., "USD")
- `risk_tolerance`: Risk level ("conservative", "moderate", or "aggressive")
- `max_position_size`: Maximum position size as a fraction of portfolio (number between 0 and 1)
- `stop_loss_percent`: Default stop loss percentage (number > 0)
- `take_profit_percent`: Default take profit percentage (number > 0)

### analysis_settings
Controls analysis parameters:
- `lookback_period_days`: Number of days to analyze (integer > 0)
- `minimum_trades_for_analysis`: Minimum number of trades required for analysis (integer > 0)
- `metrics`: List of metrics to calculate (array of strings from: "win_rate", "profit_factor", "sharpe_ratio", "max_drawdown")

### export_settings
Controls export parameters:
- `default_format`: Export format ("markdown", "html", or "pdf")
- `include_charts`: Whether to include charts in the export (boolean)
- `include_llm_insights`: Whether to include LLM insights in the export (boolean)

## Validation

The application validates the configuration file at startup and will display an error message if:
1. The configuration file is missing
2. The configuration file contains invalid JSON
3. Required sections or keys are missing
4. Values have incorrect types
5. Values are outside of valid ranges

## Error Handling

If the configuration file is invalid, the application will display a clear error message indicating what needs to be fixed.

## Example Configuration

```json
{
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
        "include_charts": true,
        "include_llm_insights": true
    }
}
```