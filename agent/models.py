from sqlalchemy.schema import CreateTable
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from database import Base

# Base = declarative_base()

class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    ip_address = Column(String(45), nullable=False)
    status = Column(String(20), default='active')
    created_at = Column(TIMESTAMP, default=datetime.utcnow().isoformat())

    metrics = relationship("SystemMetric", back_populates="server")
    actions = relationship("AutoScaleAction", back_populates="server")
    alerts = relationship("MetricAlert", back_populates="server")

class SystemMetric(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id', ondelete='CASCADE'))
    cpu_usage = Column(Numeric(5, 2))
    ram_usage = Column(Numeric(5, 2))
    disk_io = Column(Numeric(10, 2))
    net_io = Column(Numeric(10, 2))
    timestamp = Column(TIMESTAMP, default=datetime.utcnow().isoformat())

    server = relationship("Server", back_populates="metrics")

class AutoScaleAction(Base):
    __tablename__ = 'scale_actions'

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id', ondelete='SET NULL'), nullable=True)
    action_type = Column(String(50), nullable=False)
    reason = Column(Text)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow().isoformat())

    server = relationship("Server", back_populates="actions")

class MetricThreshold(Base):
    __tablename__ = 'thresholds'

    id = Column(Integer, primary_key=True)
    metric_type = Column(String(50), nullable=False)
    threshold = Column(Numeric(5, 2), nullable=False)
    direction = Column(String(10), nullable=False)
    action_type = Column(String(50), nullable=False)

class MetricAlert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id', ondelete='CASCADE'))
    metric_type = Column(String(50))
    value = Column(Numeric(10, 2))
    triggered_at = Column(TIMESTAMP, default=datetime.utcnow().isoformat())
    resolved_at = Column(TIMESTAMP, nullable=True)

    server = relationship("Server", back_populates="alerts")

# print(str(CreateTable(Server.__table__)))
# print(str(CreateTable(SystemMetric.__table__)))
# print(str(CreateTable(AutoScaleAction.__table__)))
# print(str(CreateTable(MetricThreshold.__table__)))
# print(str(CreateTable(MetricAlert.__table__)))


