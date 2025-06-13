import json
import os
import time
import psutil
import requests
import datetime
import socket
from pydantic import BaseModel


class ServerIn(BaseModel):
    name: str
    ip_address: str

class MetricIn(BaseModel):
    server_id: int
    cpu_usage: float
    ram_usage: float
    disk_io: float
    net_io: float
    timestamp: str

def get_container_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()

    print(f"Server ip is: {ip}")
    return ip

def create_server() -> dict:
    payload = ServerIn(name="metric_collector", ip_address=get_container_ip())
    try:
        response = requests.post("http://backend:8000/servers", json=payload.model_dump())
        print(f"Response: {response.json()}")
        response.raise_for_status()
        print(f"Got server_id from backend.")
        return response.json()
    except Exception as e:
        print(f"Failed to send metrics: {e}")

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
    server_id = create_server().get("id")
    # server_id = os.getenv("SERVER_ID")
    print(f"Server with id: {server_id} started.")
    while True:
        start = time.time()
        collect_and_store_metrics(int(server_id))
        elapsed = time.time() - start
        time.sleep(max(60 - elapsed, 0))
