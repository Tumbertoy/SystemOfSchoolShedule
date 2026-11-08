import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base


db = sa.create_engine(f"sqlite:///database.db")
Session = sessionmaker(bind=db, expire_on_commit=False)
Base = declarative_base()

def initDb():
    import src.systemOfSchoolSchedule.models
    Base.metadata.create_all(bind=db)
    Base.metadata.clear()



if __name__ == "__main__":
    initDb()



