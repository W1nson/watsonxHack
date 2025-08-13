
from typing import TypedDict
from langgraph.graph import add_messages
from typing_extensions import Annotated
import operator
# overall state  
class OverallState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: int 
    firstName: str
    lastName: str
    subscriptions: Annotated[list, operator.add]
    queries: Annotated[list, operator.add]