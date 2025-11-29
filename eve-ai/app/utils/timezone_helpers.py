from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Optional

# Definiujemy protokół - kontrakt wymagający istnienia created_at
def to_local_time(dt: datetime, timezone_str: str = "Europe/Warsaw") -> Optional[datetime]:
    """
    Convert datetime to local timezone.
    
    Args:
        dt: datetime in UTC
        timezone_str: timezone string (np. 'Europe/Warsaw')
        
    Returns:
        datetime in local timezone
    """
    if dt is None:
        return None
    return dt.replace(tzinfo=timezone.utc).astimezone(ZoneInfo(timezone_str))