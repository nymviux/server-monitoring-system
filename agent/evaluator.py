from models import MetricThreshold, SystemMetric, MetricAlert
from sqlalchemy.orm import Session
from datetime import datetime

def evaluate_thresholds(server_id: int, db: Session):
    thresholds = db.query(MetricThreshold).all()
    last_metric = db.query(SystemMetric).filter_by(server_id=server_id).order_by(SystemMetric.timestamp.desc()).first()

    if not last_metric:
        return

    for t in thresholds:
        value = getattr(last_metric, t.metric_type)
        if t.direction == 'above' and value > t.threshold:
            alert = MetricAlert(
                server_id=server_id,
                metric_type=t.metric_type,
                value=value,
                triggered_at=datetime.utcnow().isoformat()
            )
            db.add(alert)
            db.commit()
