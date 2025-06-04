import pandas as pd
import datetime as dt
from pathlib import Path


def load_cycle_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, delim_whitespace=True, index_col=0, parse_dates=["start_time", "end_time"])

