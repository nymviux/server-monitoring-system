
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

CPU_USAGE = Gauge("custom_cpu_usage_percent", "CPU usage percentage")
RAM_USAGE = Gauge("custom_ram_usage_percent", "RAM usage percentage")
DISK_IO = Gauge("custom_disk_io_kbs", "Disk write in KB/s")
NET_IO = Gauge("custom_net_io_kbs", "Network sent in KB/s")


def collect_and_store_metrics(server_id: int):
    db: Session = SessionLocal()
    print("Collecting metrics...")

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_io_counters().write_bytes / 1024  # KB/s
    net = psutil.net_io_counters().bytes_sent / 1024     # KB/s


    CPU_USAGE.set(cpu)
    RAM_USAGE.set(ram)
    DISK_IO.set(disk)
    NET_IO.set(net)

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
