import psutil
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import datetime

import psutil
from sqlalchemy.orm import Session
from models import SystemMetric, Server  # twoje modele
from database import SessionLocal
from datetime import datetime
from prometheus_client import Gauge, Counter


db_url = "postgresql://db:hehe123@db:5432/monitoring"

# cpu = psutil.cpu_percent(interval=1)
# ram = psutil.virtual_memory().percent
# disk = psutil.disk_io_counters().write_bytes / 1024  # KB/s
# net = psutil.net_io_counters().bytes_sent / 1024 


def collect_and_store_metrics(server_id: int):
    db: Session = SessionLocal()
    print("Collecting metrics...")

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
        timestamp=datetime.utcnow().isoformat()
    )
    db.add(metric)
    db.commit()
    db.close()
