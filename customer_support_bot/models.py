from sqlalchemy import Column, Integer, String
from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)


class CallSchedule(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(String)