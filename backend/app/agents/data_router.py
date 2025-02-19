###################################################################################
#### See https://langchain-ai.github.io/langgraph/tutorials/workflows/#routing ####
###################################################################################

from pydantic import BaseModel, Field
from typing_extensions import Literal

class Route(BaseModel):
    step: Literal["analyze", "visualize", "tabulate"] = Field(
        None, description="The next step of the data analysis agent"
    )



class DataRouter:
    def __init__(self):
        pass

    def route(self, state: dict) -> dict:
        return {
            "data_agent_type_result": "data_analyze",
        }


def data_route_decision(state: dict) -> str:
    """
    Conditional edge function to route to the appropriate node based on the state
    """
    return state.data_agent_type_result