import pickle

from schemas.event import EventList
from services.consts import CATEGORIES, DISTRICTS
from services.events_service import EventService


class AnomalyDetectorService:
    def __init__(self):
        with open('iforest', 'rb') as file:
            self.model = pickle.load(file)
        self.event_service = EventService()

    def get_anomaly_classes(self, requested_date):
        rows = self.event_service.get_events_grouped_count(requested_date)
        filtered_data = self._prepare_data_for_analysis(rows)
        data_with_anomaly = self._get_anomaly_status(filtered_data)
        return data_with_anomaly

    def set_anomaly_status_to_events(self, classes, events: EventList):
        for event in events.events:
            # 0-category, 1-district, 2-dayoff, 3-hour, 4-weather, 5-count
            is_anomaly = list(filter(lambda x: x[0] == CATEGORIES.index(event.category)
                                               and x[1] == DISTRICTS.index(event.district)
                                               and x[2] == int(event.is_day_off)
                                               and x[3] == event.hour
                                               and x[4] == event.weather,
                                     classes))[0][-1]
            event.is_anomaly = True if is_anomaly == -1 else False
        return events

    def _get_anomaly_status(self, data):
        '''
        gets a list of data like
        [Category, District, dayoff, hour, weather, count]
        returns True if its anomaly and false if its ok
        '''

        # gets 2D array
        # returns -1 if its anomaly and 1 if its ok value
        preds = self.model.predict(data).tolist()
        for i in range(len(preds)):
            data[i].append(preds[i])
        return data

    def _prepare_data_for_analysis(self, raw_data):
        data_matrix = [
            [
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            ] for row in raw_data
        ]
        return data_matrix
