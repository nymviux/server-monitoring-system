from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "postgresql://db:hehe123@db:5432/monitoring"
# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create tables
Base.metadata.create_all(bind=engine)