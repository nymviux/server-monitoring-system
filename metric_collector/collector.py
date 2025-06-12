import json
import os
import time
import psutil
import requests
import datetime
from pydantic import BaseModel

class MetricIn(BaseModel):
    server_id: int
    cpu_usage: float
    ram_usage: float
    disk_io: float
    net_io: float
    timestamp: str

def collect_and_store_metrics(server_id: int):
    print("Collecting metrics...")

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_io_counters().write_bytes / 1024  # KB/s
    net = psutil.net_io_counters().bytes_sent / 1024     # KB/s
    timestamp = datetime.datetime.utcnow().isoformat()
    
    metric_data = MetricIn(server_id=server_id, cpu_usage=cpu, ram_usage=ram, disk_io = disk, net_io=net, timestamp=timestamp)
    try:
        response = requests.post("http://backend:8000/add-metric", json=metric_data.model_dump())
        print(f"Response: {response.json()}")
        response.raise_for_status()
        print(f"Sent metrics for server {server_id}: {response.status_code}")
    except Exception as e:
        print(f"Failed to send metrics: {e}")

    
if __name__ == "__main__":
    server_id = os.getenv("SERVER_ID")
    print(f"Server with id: {server_id} started.")
    while True:
        start = time.time()
        collect_and_store_metrics(int(server_id))
        elapsed = time.time() - start
        time.sleep(max(60 - elapsed, 0))
