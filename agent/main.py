import time
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import make_asgi_app, REGISTRY, Counter
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from database import Base, SessionLocal, engine
from models import Server, SystemMetric, Base
from collector import collect_and_store_metrics
from evaluator import evaluate_thresholds
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from utils import backup_job

from apscheduler.schedulers.background import BackgroundScheduler

from crud import (
    create_server,
    get_all_metrics,
    get_server_by_id,
    make_metrics_app,
    update_server_status,
    delete_server,
    create_metric,
    get_metrics_for_server,
)

INTERVAL = 60  

Base.metadata.create_all(bind=engine)
app = FastAPI()
scheduler = BackgroundScheduler()



metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


MY_COUNTER = Counter('my_counter', 'Description of my counter')

# Expose metrics.
# def app(environ, start_response):
#     registry = CollectorRegistry()
#     multiprocess.MultiProcessCollector(registry)
#     data = generate_latest(registry)
#     status = '200 OK'
#     response_headers = [
#         ('Content-type', CONTENT_TYPE_LATEST),
#         ('Content-Length', str(len(data)))
#     ]
#     start_response(status, response_headers)
#     return iter([data])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class ServerIn(BaseModel):
    name: str
    ip_address: str

class MetricIn(BaseModel):
    server_id: int
    cpu_usage: float
    ram_usage: float
    disk_io: float
    net_io: float
    



@app.post("/servers")
def add_server(server: ServerIn, db: Session = Depends(get_db)):
    new_id = create_server(db, server.name, server.ip_address)
    return {"id": new_id}

@app.get("/servers/{server_id}")
def read_server(server_id: int, db: Session = Depends(get_db)):
    srv = get_server_by_id(db, server_id)
    if not srv:
        raise HTTPException(status_code=404, detail="Server not found")
    return {"id": srv.id, "name": srv.name, "ip_address": srv.ip_address, "status": srv.status}

@app.put("/servers/{server_id}/status")
def change_status(server_id: int, status: str, db: Session = Depends(get_db)):
    updated = update_server_status(db, server_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Server not found or no change")
    return {"status": "updated"}

@app.delete("/servers/{server_id}")
def remove_server(server_id: int, db: Session = Depends(get_db)):
    deleted = delete_server(db, server_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Server not found")
    return {"status": "deleted"}

# @app.post("/metrics")
# def submit_metric(data: MetricIn, db: Session = Depends(get_db)):
#     create_metric(db, data.server_id, data.cpu_usage, data.ram_usage, data.disk_io, data.net_io)
#     return {"status": "ok"}

# class MetricModel(BaseModel):


# @app.get("/metrics")
# def get_metrics(db: Session = Depends(get_db)) -> list[MetricModel]:
#     metrics = get_all_metrics(db)
#     if not metrics:
#         raise HTTPException(status_code=404, detail="No metrics found.")
#     print(metrics)
#     return metrics





@app.get("/metrics/{server_id}")
def list_metrics(server_id: int, db: Session = Depends(get_db)):
    return get_metrics_for_server(db, server_id)

@app.on_event("startup")
def on_startup():
    scheduler.add_job(lambda: collect_and_store_metrics(server_id=1), 'interval', seconds=15)
    scheduler.start()

@app.on_event("shutdown")
def on_shutdown():
    scheduler.shutdown()