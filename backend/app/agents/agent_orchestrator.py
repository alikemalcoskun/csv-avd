from app.models.State import State

from app.agents.data_agent import DataAgent
from app.agents.query_agent import QueryAgent
from app.agents.data_router import DataRouter, data_route_decision
from app.agents.query_evaluator import QueryEvaluator, query_eval_decision

from langgraph.graph import StateGraph, START, END
from IPython.display import Image



class AgentOrchestrator:
    def __init__(self, data_path: str, user_question: str):
        self.router_builder = StateGraph(State)
        self.workflow = None

        # Agents
        self.query_agent = QueryAgent()
        self.data_agent = DataAgent()
        self.data_router = DataRouter()
        self.query_evaluator = QueryEvaluator()

    def generate_workflow(self) -> StateGraph:
        # Add nodes
        self.router_builder.add_node("query_generate", self.query_agent.generate)
        self.router_builder.add_node("query_execute", self.query_agent.execute)
        self.router_builder.add_node("query_eval", self.query_evaluator.evaluate)
        self.router_builder.add_node("data_agent_route", self.data_router.route)
        self.router_builder.add_node("data_analyze", self.data_agent.analyze)
        self.router_builder.add_node("data_visualize", self.data_agent.visualize)
        self.router_builder.add_node("data_tabulate", self.data_agent.tabulate)

        # Add edges to connect nodes
        self.router_builder.add_edge(START, "query_generate")
        self.router_builder.add_edge("query_generate", "query_execute")
        self.router_builder.add_edge("query_execute", "query_eval")
        self.router_builder.add_conditional_edges("query_eval", query_eval_decision, {
            "pass": "data_agent_route",
            "fail": "query_generate",
            "max_retries_exceeded": END,
        })
        self.router_builder.add_conditional_edges(
            "data_agent_route",
            data_route_decision,
            {
                "data_analyze": "data_analyze",
                "data_visualize": "data_visualize",
                "data_tabulate": "data_tabulate",
            },
        )
        self.router_builder.add_edge("data_analyze", END)
        self.router_builder.add_edge("data_visualize", END)
        self.router_builder.add_edge("data_tabulate", END)

    def compile_workflow(self):
        # Compile workflow
        self.workflow = self.router_builder.compile()

    def invoke(self, state):
        # Invoke workflow
        return self.workflow.invoke(state)

    def draw_workflow(self):
        # Show the workflow
        img = Image(self.workflow.get_graph().draw_mermaid_png())
        with open("workflow.png", "wb") as f:
            f.write(img.data)