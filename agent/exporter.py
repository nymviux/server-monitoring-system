from prometheus_client import start_http_server, Gauge
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import SystemMetric
import time
import psutil

cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory().percent
disk = psutil.disk_io_counters().write_bytes / 1024  # KB/s
net = psutil.net_io_counters().bytes_sent / 1024 


def update_metrics():
    db: Session = SessionLocal()
    metric = db.query(SystemMetric).order_by(SystemMetric.timestamp.desc()).first()

    if metric:
        cpu.set(float(metric.cpu_usage))
        ram.set(float(metric.ram_usage))
        disk.set(float(metric.disk_io))
        net.set(float(metric.net_io))

    db.close()


if __name__ == '__main__':
    start_http_server(8000)
    while True:
        update_metrics()
        time.sleep(10)
