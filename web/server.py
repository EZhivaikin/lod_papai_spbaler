import uvicorn
from fastapi import FastAPI

from services.anomaly_detector_service import AnomalyDetectorService
from services.events_service import EventService


app = FastAPI()

anomaly_detector = AnomalyDetectorService()
event_service = EventService()


@app.get('/year/{year}/month/{month}/day/{day}')
async def get_actual_data(
        year: int, month: int, day: int
):
    requested_date = f'{year:02d}-{month:02d}-{day:02d}'
    events = event_service.get_events_by_date(requested_date)
    classes = anomaly_detector.get_anomaly_classes(requested_date)
    events = anomaly_detector.set_anomaly_status_to_events(classes, events)
    return events


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
