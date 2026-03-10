from database import SessionLocal
from models import Order, Ticket, CallSchedule

db = SessionLocal()

# Insert Orders
orders = [
    Order(id=1, status="Processing"),
    Order(id=2, status="Shipped"),
    Order(id=3, status="Delivered")
]

# Insert Tickets
tickets = [
    Ticket(status="Payment issue"),
    Ticket(status="Package damaged"),
]

# Insert Call Schedules
calls = [
    CallSchedule(time="2026-03-10 10:00 AM"),
    CallSchedule(time="2026-03-11 04:30 PM"),
]

db.add_all(orders)
db.add_all(tickets)
db.add_all(calls)

db.commit()
db.close()

print("Sample data inserted successfully!")