import pandas as pd
from typing import List
from src.models.trade import Trade
from datetime import datetime
import logging
import re

REQUIRED_COLUMNS = [
    "Symbol", "Price", "Time", "Order #", "Description", "Expiry", "Strike", "OptionType", "Side", "Quantity"
]

class CSVProcessor:
    """
    Handles loading, validating, and processing TastyTrade CSV files.
    """
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None

    def load_csv(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.csv_path)
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise FileNotFoundError(f"File not found: '{self.csv_path}'")
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")
            raise PermissionError(f"Permission denied: cannot read '{self.csv_path}'")
        except Exception as e:
            logging.error(f"Failed to read CSV: {e}")
            raise ValueError(f"Failed to read CSV: {e}")
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            logging.error(f"Missing required columns: {missing}")
            raise ValueError(f"Missing required columns: {missing}")
        self.df = df
        return df

    def validate(self) -> bool:
        if self.df is None:
            self.load_csv()
        missing = [col for col in REQUIRED_COLUMNS if col not in self.df.columns]
        if missing:
            logging.error(f"Missing required columns: {missing}")
            return False
        return True

    def to_trades(self) -> List[Trade]:
        if self.df is None:
            self.load_csv()
        trades = []
        order_ids = set()
        symbol_pattern = re.compile(r"^[A-Z]{1,5}$")
        # Accept timestamps with or without seconds
        time_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
        
        for idx, row in self.df.iterrows():
            try:
                # Check for required fields in row
                for col in REQUIRED_COLUMNS:
                    if pd.isna(row.get(col, None)):
                        raise ValueError(f"Missing value for required field '{col}' in row {idx}")
                
                # Validate symbol
                symbol = row["Symbol"]
                if not symbol_pattern.match(symbol):
                    raise ValueError(f"Invalid symbol '{symbol}' in row {idx}")
                
                # Validate time format
                time_str = str(row["Time"])
                try:
                    # Try each format until one succeeds
                    parsed_time = None
                    for fmt in time_formats:
                        try:
                            parsed_time = datetime.strptime(time_str, fmt)
                            break
                        except ValueError:
                            continue
                    if parsed_time is None:
                        raise ValueError(f"Invalid timestamp format '{time_str}' in row {idx}")
                except ValueError:
                    raise ValueError(f"Invalid timestamp format '{time_str}' in row {idx}")
                
                # Validate order_id uniqueness
                order_id = str(row["Order #"]).replace("#", "").strip()
                if order_id in order_ids:
                    raise ValueError(f"Duplicate order number '{order_id}' in row {idx}")
                order_ids.add(order_id)
                
                # Parse price
                price = self._parse_price(row["Price"])
                if price is None:
                    raise ValueError(f"Invalid price '{row['Price']}' in row {idx}")
                
                # Create trade
                trade = Trade(
                    order_id=order_id,
                    symbol=symbol,
                    expiry=str(row["Expiry"]),
                    strike=float(row["Strike"]),
                    option_type=row["OptionType"],
                    side=row["Side"],
                    quantity=int(row["Quantity"]),
                    price=price,
                    time=time_str,
                )
                
                # Validate trade
                if not trade.validate():
                    raise ValueError(f"Trade validation failed for row {idx}")
                
                trades.append(trade)
            except Exception as e:
                logging.warning(f"Skipping malformed row {idx}: {e}")
        return trades

    @staticmethod
    def _parse_price(price_str):
        # Remove 'cr'/'db' and convert to float
        if isinstance(price_str, str):
            price_str = price_str.replace('cr', '').replace('db', '').strip()
        try:
            return float(price_str)
        except Exception:
            return None 