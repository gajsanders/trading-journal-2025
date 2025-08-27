import pandas as pd
from typing import Optional, Dict, Any
from src.processors.csv_processor import CSVProcessor
from src.processors.duplicate_detector import DuplicateDetector
from src.models.trade import Trade
from src.app.ui_components import progress_component

class DataHandler:
    """
    Handles data processing: CSV loading, duplicate detection, trade parsing/linking, and progress updates.
    """
    def __init__(self):
        self.trades: Optional[list] = None
        self.duplicates: Optional[pd.DataFrame] = None
        self.progress: float = 0.0

    def process_csv(self, file) -> Dict[str, Any]:
        self.progress = 0.1
        progress_component(self.progress, "Loading CSV...")
        processor = CSVProcessor(file)
        df = processor.load_csv()
        self.progress = 0.3
        progress_component(self.progress, "Detecting duplicates...")
        dup_detector = DuplicateDetector(df)
        self.duplicates = dup_detector.find_duplicates()
        self.progress = 0.5
        progress_component(self.progress, "Parsing trades...")
        self.trades = processor.to_trades()
        self.progress = 0.8
        progress_component(self.progress, "Linking trades...")
        # Placeholder for linking logic
        self.progress = 1.0
        progress_component(self.progress, "Done!")
        return {
            'df': df,
            'duplicates': self.duplicates,
            'trades': self.trades
        } 