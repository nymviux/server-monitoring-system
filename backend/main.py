from fastapi import FastAPI
from pydantic import BaseModel
from .models import Metric, Base
from .database import engine, SessionLocal
from .erd import erd_png
from fastapi.responses import FileResponse


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
    metric = Metric(**data.dict())
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

@app.get("/erd", response_class=FileResponse)
def get_erd():
    png_file = erd_png()
    return FileResponse(png_file, media_type="image/png", filename="erd.png")
