from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class State(BaseModel):
    # Input states
    user_question: str = Field(default="")
    data: str = Field(default="")

    # Generation states
    query_generate_result: Dict[str, Any] = Field(default_factory=dict)
    query_execute_result: Dict[str, Any] = Field(default_factory=dict)
    query_fix_result: Dict[str, Any] = Field(default_factory=dict)
    
    # Data agent states
    data_analyze_result: Dict[str, Any] = Field(default_factory=dict)
    data_visualize_result: Dict[str, Any] = Field(default_factory=dict)
    data_tabulate_result: Dict[str, Any] = Field(default_factory=dict)

    # Routing states
    # https://langchain-ai.github.io/langgraph/tutorials/workflows/#routing
    data_agent_type_result: str = Field(default="data_analyze")
    
    # Evaluator states
    # https://langchain-ai.github.io/langgraph/tutorials/workflows/#evaluator-optimizer
    query_eval_result: str = Field(default="pass")
    query_eval_retries: int = Field(default=0)