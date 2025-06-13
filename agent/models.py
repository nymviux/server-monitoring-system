from sqlalchemy.schema import CreateTable
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from database import Base

class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    ip_address = Column(String(45), nullable=False)
    status = Column(String(20), default='active')
    created_at = Column(TIMESTAMP, default=datetime.utcnow().isoformat())

    metrics = relationship("SystemMetric", back_populates="server")

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
