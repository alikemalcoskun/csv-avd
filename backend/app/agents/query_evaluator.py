###############################################################################################
#### See https://langchain-ai.github.io/langgraph/tutorials/workflows/#evaluator-optimizer ####
###############################################################################################

class QueryEvaluator:
    def __init__(self):
        pass
    
    def evaluate(self, state: dict) -> dict:
        if state.query_eval_retries > 2:
            return {
                "query_eval_result": "max_retries_exceeded",
            }
        
        query_result = state.query_execute_result
        if query_result.get("error"):
            return {
                "query_eval_result": "fail",
                "query_eval_retries": state.query_eval_retries + 1,
                }
        
        return {
            "query_eval_result": "pass",
            "query_eval_retries": state.query_eval_retries + 1,
            }


def query_eval_decision(state: dict) -> str:
    return state.query_eval_result