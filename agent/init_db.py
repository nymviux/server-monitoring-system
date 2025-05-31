from database import SessionLocal
from models import Server, MetricThreshold


def seed_database():
    db = SessionLocal()
    server = Server(name="localhost", ip_address="127.0.0.1")
    db.add(server)
    db.commit()

    thresholds = [
        MetricThreshold(metric_type="cpu_usage", threshold=70.0, direction="above", action_type="scale_up"),
        MetricThreshold(metric_type="ram_usage", threshold=80.0, direction="above", action_type="scale_up"),
    ]
    db.add_all(thresholds)
    db.commit()
    db.close()


if __name__ == '__main__':
    seed_database()

