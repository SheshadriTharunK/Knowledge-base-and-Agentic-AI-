from langchain.tools import tool
from services import (
    fetch_order_status,
    create_support_ticket,
    schedule_support_call,
    display_all_orders
)


@tool
def get_order_status(order_id: int) -> str:
    """Retrieve order status"""
    return fetch_order_status(order_id)

@tool
def create_ticket(id: int, status: str) -> str:
    """Create support ticket"""
    return create_support_ticket(id, status)


@tool
def schedule_call(time: str) -> str:
    """Schedule support call"""
    return schedule_support_call(time)