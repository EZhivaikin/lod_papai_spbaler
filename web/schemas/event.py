from typing import List, Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    lat: float
    lon: float
    category: str
    district: str
    is_anomaly: Optional[bool]
    weather: Optional[float]
    is_day_off: Optional[bool]


class Event(EventBase):
    hour: int
    pass


class EventList(BaseModel):
    events: List[Event]
