
import psutil
from sqlalchemy.orm import Session
from models import SystemMetric
from database import SessionLocal
from datetime import datetime

def collect_and_store_metrics(server_id: int):
    db: Session = SessionLocal()

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_io_counters().write_bytes / 1024  # KB/s
    net = psutil.net_io_counters().bytes_sent / 1024     # KB/s

    metric = SystemMetric(
        server_id=server_id,
        cpu_usage=cpu,
        ram_usage=ram,
        disk_io=disk,
        net_io=net,
        timestamp=datetime.utcnow()
    )
    db.add(metric)
    db.commit()
    db.close()
