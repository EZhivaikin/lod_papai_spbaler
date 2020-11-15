import sqlite3

from schemas.event import Event, EventList
from services.consts import CATEGORIES, DISTRICTS


class EventService:
    def __init__(self):
        self._conn = sqlite3.connect("events.db")
        self._cursor = self._conn.cursor()

    def get_events_grouped_count(self, requested_date):
        self._cursor.execute(f'''
            SELECT category, district, dayoff, hour, weather, count(*)  FROM event 
            WHERE date(event.date) BETWEEN date(?) and date(?)
            GROUP BY event.date, event.hour,  event.district, event.category
        ''', (requested_date, requested_date))
        rows = self._cursor.fetchall()

        return rows

    def get_events_by_date(self, requested_date):
        self._cursor.execute(f'''
            SELECT * FROM event WHERE date(date) 
            BETWEEN date(?) and date(?);
        ''', (requested_date, requested_date))
        rows = self._cursor.fetchall()
        events = [Event(
            lat=row[2],
            lon=row[3],
            hour=row[6],
            category=CATEGORIES[row[1]],
            district=DISTRICTS[row[4]],
            weather=row[8],
            is_day_off=True if row[7] == 1 else False
        ) for row in rows]
        events_list = EventList(events=events)
        return events_list
