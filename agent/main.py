
import time

from fastapi import FastAPI
from pydantic import BaseModel
from database import Base, SessionLocal, engine
from models import Server, SystemMetric, Base
from collector import collect_and_store_metrics
from evaluator import evaluate_thresholds
from fastapi.responses import FileResponse

INTERVAL = 60  # seconds

Base.metadata.create_all(bind=engine)
app = FastAPI()

class MetricIn(BaseModel):
    server_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: float

@app.post("/metrics")
def submit_metric(data: MetricIn):
    db = SessionLocal()
    metric = SystemMetric(**data.dict())
    db.add(metric)
    db.commit()
    db.close()
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "FastAPI is running. Visit /erd to generate ER diagram."}

# @app.get("/erd", response_class=FileResponse)
# def get_erd():
#     png_file = erd_png()
#     return FileResponse(png_file, media_type="image/png", filename="erd.png")

if __name__ == "__main__":
    db = SessionLocal()
    servers = db.query(Server).all()

    while True:
        for server in servers:
            collect_and_store_metrics(server.id)
            evaluate_thresholds(server.id, db)
        time.sleep(INTERVAL)

    db.close()