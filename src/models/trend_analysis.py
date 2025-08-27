from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional

class PerformanceTrend(Enum):
    UP = auto()
    DOWN = auto()
    FLAT = auto()
    OUTLIER = auto()
    UNKNOWN = auto()

@dataclass
class TrendAnalysis:
    trend: PerformanceTrend
    significance: Optional[float] = None
    outliers: List[float] = field(default_factory=list)
    trend_data: List[float] = field(default_factory=list)
    description: Optional[str] = None 