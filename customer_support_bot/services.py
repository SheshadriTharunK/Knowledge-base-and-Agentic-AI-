from database import SessionLocal
from models import Order, Ticket, CallSchedule
import json


def fetch_order_status(order_id: int):

    db = SessionLocal()

    order = db.query(Order).filter(Order.id == order_id).first()

    db.close()

    if order:
        return f"Order status: {order.status}"

    return "Order not found"


def create_support_ticket(ticket_id: int, status: str):

    db = SessionLocal()

    ticket = Ticket(
        id=ticket_id,
        status=status
    )

    db.add(ticket)
    db.commit()

    db.close()

    return f"Ticket {ticket_id} created with status {status}"


def schedule_support_call(time: str):

    db = SessionLocal()

    call = CallSchedule(time=time)

    db.add(call)
    db.commit()
    db.refresh(call)

    db.close()

    return f"Call scheduled at {call.time}"

def display_all_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()

    if not orders:
        return "No orders found."

    return "\n".join([f"Order ID: {order.id}, Status: {order.status}" for order in orders])