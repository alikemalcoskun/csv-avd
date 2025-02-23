###################################################################################
#### See https://langchain-ai.github.io/langgraph/tutorials/workflows/#routing ####
###################################################################################

from pydantic import BaseModel, Field
from typing_extensions import Literal
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_service import LLMService

class Route(BaseModel):
    step: Literal["data_analyze", "data_visualize", "data_tabulate", "data_machine_learning"] = Field(
        None, description="The next step of the data analysis agent"
    )



class DataRouter:
    def __init__(self):
        self.llm = LLMService()

    def route(self, state: dict) -> dict:
        messages = [
            ("system", '''Analyze the user question to determine the type of data analysis to perform.
            - Data analysis types:
                - Analyze: Analyzes the data and generates a report.
                    - Examples: "What is the total sales in the data?", "Gimme a report about the transactions last month."
                - Visualize: Visualize the data according to the user question.
                    - Examples: "Plot the sales over time.", "Show me a chart of the sales by product."
                - Tabulate: Reconstruct the data in a tabular format to show the data on a table.
                    - Examples: "Show me the data in a table.", "List the sales by product."
                - Machine Learning: Perform machine learning on the data to predict or classify the data.
                    - Examples: "Predict the sales for next month.", "Classify the transactions by product."
            '''),
            ("human", '''- User question: {user_question}
            ''')
        ]
        prompt = ChatPromptTemplate(messages)

        response = self.llm.invoke(prompt, is_response_json=False, structured_output=Route,
            input={
                "user_question": state.user_question
            }
        )

        return {
            "data_agent_type_result": response.step
        }



def data_route_decision(state: dict) -> str:
    """
    Conditional edge function to route to the appropriate node based on the state
    """
    return state.data_agent_type_result