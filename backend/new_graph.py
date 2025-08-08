from database.database import SessionLocal
from sqlalchemy import text

from typing import TypedDict
from langgraph.graph import add_messages
from typing_extensions import Annotated
import operator
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from llm import watsonx_model

# overall state  
class OverallState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: int 
    firstName: str
    lastName: str
    subscriptions: Annotated[list, operator.add]




def get_user_subscription(state: OverallState):
    db = SessionLocal()
    user_id = state["user_id"]
    out = db.execute(text(f"""SELECT 
    s.start_date as subscription_start,
    s.current_status as subscription_status,
    st.tier_name,
    st.price_usd,
    sv.name as service_name,
    sv.category
    FROM users u
    LEFT JOIN subscriptions s ON u.id = s.user_id
    LEFT JOIN service_tiers st ON s.tier_id = st.id
    LEFT JOIN services sv ON st.service_id = sv.id
    WHERE u.id = {user_id};"""))

    subscriptions = []
    rows_as_dicts = [row._asdict() for row in out]
    for row_dict in rows_as_dicts:
        subscriptions.append(row_dict)

    out = db.execute(text(f"""SELECT 
    u.firstName,
    u.lastName
    FROM users u
    WHERE u.id = {user_id};"""))
    out = [row._asdict() for row in out]
    firstName = out[0]["firstName"]
    lastName = out[0]["lastName"]
    
    return {'subscriptions': subscriptions, "firstName": firstName, "lastName": lastName}




def agent_review_user_subscription(state: OverallState):
    # configurable = Configuration.from_runnable_config(config)
    firstName = state["firstName"]
    question = state["messages"][0].content
    subscription_history = state["subscriptions"]

    column = "service_name | category | tier_name | price_usd | subscription_start | subscription_status\n"
    format_subscription_history = column + "\n".join([f"{sub['service_name']} | {sub['category']} | {sub['tier_name']} | {sub['price_usd']} | {sub['subscription_start']} | {sub['subscription_status']}" for sub in subscription_history])
    # print(format_subscription_history)
    subscription_analysis_prompt = f"""
You are a helpful financial assistant. Your job is to analyze the user's subscription history and recommend ways to reduce their monthly spending.
Here is the user's subscription history:
    {format_subscription_history}

Based on the provided subscription data, do the following:
    1.	Usage Analysis

    •	Determine if the user is actively using each subscription (based on any usage data if available).
    •	If usage is not provided, don't make assumptions.

    2.	Cost Efficiency Evaluation

    •	Identify the most expensive subscriptions.
    •	Determine whether each subscription appears to offer good value for the price.

    3.	Cheaper Alternatives

    •	Search online for cheaper alternatives with similar features (e.g., if the user pays for Spotify, check for cheaper music services or free versions).
    •	Provide relevant names and estimated prices of those services.

    4.	Cancellation Suggestions

    •	If a service is rarely or never used, or is overpriced compared to alternatives, suggest canceling it.

    5.	Summary of Actions

    •	Summarize in clear, actionable steps:
    •	Which subscriptions to keep, cancel, or replace (and with what).
    •	Total estimated monthly savings if recommendations are followed.

When generating your response:
    •	Be concise but informative.
    •	Use bullet points for clarity.
    •	Be neutral and helpful, DO NOT shame the user for spending.
    •	Use the user name to respond to the user casually: {firstName}. 
    •	At the end, please offer user the recommandation actions that you have suggested.

    Question: {question}
    """    

    # if "ibm" in configurable.subscription_analysis_model:
    #     llm = watsonx_model
    # else:
    #     llm = ollama_model

    llm = watsonx_model
    message = llm.invoke(subscription_analysis_prompt)

    return {'messages': message, 'subscription_suggestion': message}




builder = StateGraph(OverallState)

builder.add_node("get_user_subscription", get_user_subscription)
builder.add_node("agent_review_user_subscription", agent_review_user_subscription)


builder.add_edge(START, "get_user_subscription")
builder.add_edge("get_user_subscription", "agent_review_user_subscription")
builder.add_edge("agent_review_user_subscription", END)

agent = builder.compile(name="finance-budget-search-agent")
