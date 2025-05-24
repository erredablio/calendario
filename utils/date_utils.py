# utils/date_utils.py
from datetime import datetime
from typing import Optional

def parse_date(date_str: str) -> Optional[datetime.date]:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

