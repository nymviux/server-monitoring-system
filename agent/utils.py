import os
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import datetime

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
BACKUP_DIR = os.getenv("BACKUP_DIR", "./backups")




def backup_job():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{DB_NAME}_backup_{timestamp}.sql"
    filepath = os.path.join(BACKUP_DIR, filename)

    print(f"Tworzenie backupu bazy: {filepath}")

    try:
        # Eksport zmiennej do środowiska (pg_dump jej potrzebuje)
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASSWORD

        # Uruchomienie dumpa
        subprocess.run(
            [
                "pg_dump",
                "-U", DB_USER,
                "-h", DB_HOST,
                "-d", DB_NAME,
                "-F", "c",  
                "-f", filepath
            ],
            check=True,
            env=env
        )
        print("Backup succes.")

    except subprocess.CalledProcessError as e:
        print(f"error: {e}")

