"""
Script to generate large datasets for performance testing of the Trading Journal application.

This script creates CSV files with varying sizes of trade data (from 10,000 to 1,000,000 entries)
to evaluate the application's performance with large datasets.
"""

import csv
import random
import string
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("tests/performance/datasets")
OUTPUT_DIR.mkdir(exist_ok=True)

# Trade data configuration
SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "AMD", "INTC", "ORCL"]
OPTION_TYPES = ["Call", "Put"]
SIDES = ["BTO", "STC", "BTC", "STO"]
EXPIRY_DAYS = [14, 30, 60, 90, 180]  # Days until expiry

# Performance thresholds (in seconds)
THRESHOLDS = {
    "csv_processing": 30,  # Max time to process CSV file
    "trade_analysis": 60,   # Max time to analyze trades
    "llm_insights": 120,    # Max time to generate LLM insights
    "chart_generation": 180, # Max time to generate charts
    "report_assembly": 90,   # Max time to assemble report
    "total_workflow": 300   # Max time for complete workflow
}

def random_string(length=8):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_date(start_date="2024-01-01", end_date="2024-12-31"):
    """Generate a random date between start and end dates."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d %H:%M")

def random_strike_price(symbol):
    """Generate a random strike price based on the symbol."""
    base_prices = {"AAPL": 150, "MSFT": 300, "GOOGL": 2500, "AMZN": 3000, "TSLA": 250, "NVDA": 800, "META": 400, "AMD": 200, "INTC": 50, "ORCL": 100}
    base = base_prices.get(symbol, 100)
    return round(base + random.uniform(-50, 50), 2)

def random_price(symbol):
    """Generate a random price based on the symbol."""
    base_prices = {"AAPL": 2.5, "MSFT": 1.8, "GOOGL": 3.2, "AMZN": 2.8, "TSLA": 4.1, "NVDA": 2.2, "META": 3.5, "AMD": 1.5, "INTC": 0.8, "ORCL": 1.2}
    base = base_prices.get(symbol, 1.0)
    return round(base + random.uniform(-0.5, 0.5), 2)

def generate_trade_data():
    """Generate a single trade entry."""
    symbol = random.choice(SYMBOLS)
    price = random_price(symbol)
    time = random_date()
    order_id = random_string(6)
    description = f"Buy {random.choice(OPTION_TYPES)}" if random.random() < 0.7 else f"Buy {random.choice(SYMBOLS)} stock"
    expiry_days = random.choice(EXPIRY_DAYS)
    expiry = (datetime.strptime(time.split()[0], "%Y-%m-%d") + timedelta(days=expiry_days)).strftime("%Y-%m-%d")
    strike = random_strike_price(symbol)
    option_type = random.choice(OPTION_TYPES)
    side = random.choice(SIDES)
    quantity = random.randint(1, 10)

    return {
        "Symbol": symbol,
        "Price": price,
        "Time": time,
        "Order #": order_id,
        "Description": description,
        "Expiry": expiry,
        "Strike": strike,
        "OptionType": option_type,
        "Side": side,
        "Quantity": quantity
    }

def create_large_dataset(size, filename):
    """Create a large dataset with the specified number of trades."""
    print(f"Creating dataset with {size} trades: {filename}")

    # Create the output directory if it doesn't exist
    output_path = OUTPUT_DIR / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the dataset to CSV
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ["Symbol", "Price", "Time", "Order #", "Description", "Expiry", "Strike", "OptionType", "Side", "Quantity"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write trades
        for _ in range(size):
            trade = generate_trade_data()
            writer.writerow(trade)

    print(f"Dataset created: {output_path}")
    return output_path

def main():
    """Main function to generate large datasets."""
    # Create datasets of various sizes
    sizes = [10000, 50000, 100000, 500000, 1000000]

    for size in sizes:
        filename = f"large_trades_{size}.csv"
        create_large_dataset(size, filename)

    # Save thresholds to a file for reference
    thresholds_path = OUTPUT_DIR / "performance_thresholds.json"
    with open(thresholds_path, 'w') as f:
        import json
        json.dump(THRESHOLDS, f, indent=2)

    print(f"Performance thresholds saved to: {thresholds_path}")

if __name__ == "__main__":
    main()
