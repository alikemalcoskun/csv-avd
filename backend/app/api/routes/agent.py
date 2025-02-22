from fastapi import APIRouter, status, HTTPException
from app.models.agent import AgentRequest, AgentResponse

import json
from app.services.data_service import DataService
from app.agents.agent_orchestrator import AgentOrchestrator
from app.models.State import State

from loguru import logger


router = APIRouter()

@router.post(
        path="/run",
        name="Agent Workflow Run",
        description=(
            "Run the agents orchestrator to analyze the data."
        ),
        response_description="The status of the service.",
        status_code=status.HTTP_200_OK,
        response_model=AgentResponse)
def run_workflow(request: AgentRequest):
    if not request.user_question or request.user_question == "":
        raise HTTPException(status_code=400, detail="No user question provided.")

    data = get_data(request.data, request.use_default_data)
    if not data or data == '""':
        raise HTTPException(status_code=400, detail="No data provided.")

    orchestrator = AgentOrchestrator()
    orchestrator.generate_workflow()
    orchestrator.compile_workflow()

    initial_state = State(data=data, user_question=request.user_question)
    state_dict = orchestrator.invoke(initial_state.model_dump())
    state = State(**state_dict)  # Convert dictionary back to State model

    data_agent_type_result = state.data_agent_type_result
    if data_agent_type_result == "data_analyze":
        result = state.data_analyze_result
    elif data_agent_type_result == "data_visualize":
        result = state.data_visualize_result
    elif data_agent_type_result == "data_tabulate":
        result = state.data_tabulate_result
    else:
        raise HTTPException(status_code=500, detail="No data agent type result provided.")

    return AgentResponse(user_question=request.user_question, result=result)


def get_data(data: dict, use_default_data: bool) -> str:
    if use_default_data:
        data_path = "data/Stock_Trading_History.csv"
        data = DataService().from_csv_file(data_path)
        data = json.dumps(data.to_json())
    return data
