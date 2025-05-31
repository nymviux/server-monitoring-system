from sqlalchemy.orm import Session
from models import Server, SystemMetric, MetricThreshold, MetricAlert
from datetime import datetime


def create_server(db: Session, name: str, ip_address: str) -> int:
    new_server = Server(name=name, ip_address=ip_address)
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server.id

def get_server_by_id(db: Session, server_id: int):
    return db.query(Server).filter(Server.id == server_id).first()

def update_server_status(db: Session, server_id: int, new_status: str) -> bool:
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        return False
    server.status = new_status
    db.commit()
    return True

def delete_server(db: Session, server_id: int) -> bool:
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        return False
    db.delete(server)
    db.commit()
    return True

# Metric CRUD

def create_metric(db: Session, server_id: int, cpu: float, ram: float, disk: float, net: float) -> int:
    new_metric = SystemMetric(
        server_id=server_id,
        cpu_usage=cpu,
        ram_usage=ram,
        disk_io=disk,
        net_io=net,
        timestamp=datetime.utcnow()
    )
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric.id

def get_metrics_for_server(db: Session, server_id: int):
    return db.query(SystemMetric).filter(SystemMetric.server_id == server_id).order_by(SystemMetric.timestamp.desc()).all()
