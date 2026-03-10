from mcp.client import MCPClient

# connect to MCP server
client = MCPClient("http://localhost:8000")


def fetch_order_status(order_id: str):
    return client.call_tool(
        "fetch_order_status",
        {"order_id": order_id}
    )


def create_support_ticket(details: str):
    return client.call_tool(
        "create_support_ticket",
        {"details": details}
    )


def schedule_support_call(time: str):
    return client.call_tool(
        "schedule_support_call",
        {"time": time}
    )