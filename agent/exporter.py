from prometheus_client import start_http_server, Gauge
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import SystemMetric
import time

cpu_gauge = Gauge('cpu_usage', 'CPU usage percentage')
ram_gauge = Gauge('ram_usage', 'RAM usage percentage')
disk_gauge = Gauge('disk_io', 'Disk IO (KB)')
net_gauge = Gauge('net_io', 'Network IO (KB)')


def update_metrics():
    db: Session = SessionLocal()
    metric = db.query(SystemMetric).order_by(SystemMetric.timestamp.desc()).first()

    if metric:
        cpu_gauge.set(float(metric.cpu_usage))
        ram_gauge.set(float(metric.ram_usage))
        disk_gauge.set(float(metric.disk_io))
        net_gauge.set(float(metric.net_io))

    db.close()


if __name__ == '__main__':
    start_http_server(8000)
    while True:
        update_metrics()
        time.sleep(10)
