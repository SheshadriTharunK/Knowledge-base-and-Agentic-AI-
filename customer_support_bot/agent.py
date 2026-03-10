import json 

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

from system_prompt import system_prompt
from retriever import build_context, vector_db

load_dotenv( override = True )

from tools import (
    create_ticket,
    get_order_status,
    schedule_call
)


llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def initialize_knowledge_agent():

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    agent = create_agent(
        llm,
        tools=[],   # IMPORTANT: no tools
        system_prompt=system_prompt
    )
    
    return agent

def initialize_order_agent():

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    tools = [
        create_ticket,
        get_order_status,
        schedule_call
    ]

    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=system_prompt
    )
    return agent 



def judge_query(query):

    prompt = f"""
You are a query classifier.

Classify the user query into ONE category.

knowledge:
Questions about company services, FAQs, policies, contact info, location, or general company information.

orders:
Questions about order tracking, shipment, refunds, cancellations, invoices, or delivery.

User query:
{query}

Return JSON only:

{{
 "result_type": "knowledge" OR "orders"
}}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)["result_type"]
    except:
        return "knowledge"

knowledge_agent = initialize_knowledge_agent()
order_agent = initialize_order_agent()

def handle_query(query):

    query_type = judge_query(query)
    print("Query type (Classifying the type of query whether it's a knowledge or order query):", query_type)
    if query_type == "knowledge":

        # Retrieve RAG context
        context = build_context(
            vector_db=vector_db,
            query=query,
            top_k=4
        )

        query_with_context = f"""
<context>
{context}
</context>

User question:
{query}
"""
        print("Query with RAG context added:", query_with_context)
        response = knowledge_agent.invoke({
            "messages": [{"role": "user", "content": query_with_context}]
        })

    else:

        response = order_agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        message = response["messages"][-1].content
        try:
            tool_call = json.loads(message)
            print("Tool call detected:", tool_call)

            tool_name = tool_call.get("name")
            params = tool_call.get("parameters", {})

            ticket_id = params.get("id")
            ticket_status = params.get("status")

            print(
                "Extracted tool call details - Tool Name:",
                tool_name,
                "Ticket Status:",
                ticket_status,
                "Ticket ID:",
                ticket_id
            )
            if tool_name == "Create support ticket":

                return create_ticket.invoke({
                    "id": ticket_id,
                    "status": ticket_status
                })

            if tool_name == "Retrieve order status":
                return get_order_status.invoke(params)

            if tool_name == "Schedule support call":
                return schedule_call.invoke(params)

        except Exception as e:
            print("No tool execution needed:", e)

        return message

    return response["messages"][-1].content


