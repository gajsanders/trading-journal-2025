import pandas as pd
import logging
from typing import List, Dict, Any

class DuplicateDetector:
    """
    Detects duplicate Order # entries in TastyTrade CSV data.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def find_duplicates(self) -> pd.DataFrame:
        """Return DataFrame of rows with duplicate Order #."""
        if "Order #" not in self.df.columns:
            logging.error("Order # column missing from data.")
            raise ValueError("Order # column missing from data.")
        # Remove '#' if present in Order #
        self.df["Order # Clean"] = self.df["Order #"].astype(str).str.replace('#', '').str.strip()
        dupes = self.df[self.df.duplicated("Order # Clean", keep=False)]
        return dupes

    def duplicate_summary(self) -> Dict[str, Any]:
        """Return summary statistics for duplicate Order # entries."""
        dupes = self.find_duplicates()
        num_duplicates = dupes["Order # Clean"].nunique()
        total_records = len(dupes)
        summary = {
            "num_duplicate_order_numbers": num_duplicates,
            "total_duplicate_records": total_records,
            "duplicate_order_numbers": dupes["Order # Clean"].unique().tolist(),
        }
        return summary

    def structured_results(self) -> Dict[str, Any]:
        """Return structured results for UI display."""
        summary = self.duplicate_summary()
        dupes = self.find_duplicates()
        records = dupes.to_dict(orient="records")
        return {
            "summary": summary,
            "duplicate_records": records,
        } 