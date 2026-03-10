from database import engine
from models import Base, Order, Ticket, CallSchedule

Base.metadata.create_all(bind=engine)