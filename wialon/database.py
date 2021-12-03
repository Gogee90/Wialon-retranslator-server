from sqlalchemy import create_engine, Sequence, Integer, Column, DateTime, DECIMAL, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///sqlite3.db')
Base = declarative_base()


class Points(Base):
    __tablename__ = 'Points'
    point_id = Column(Integer, Sequence('point_seq'), primary_key=True)
    device_id = Column(Integer)
    point_time = Column(DateTime)
    latitude = Column(DECIMAL)
    longitude = Column(DECIMAL)
    entire_result = Column(String)


Base.metadata.create_all(engine)
