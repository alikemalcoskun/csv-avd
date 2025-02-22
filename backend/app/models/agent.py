from pydantic import BaseModel


class AgentRequest(BaseModel):
    user_question: str = ""
    data: str = ""
    use_default_data: bool = False

class AgentResponse(BaseModel):
    user_question: str = ""
    result: dict = {}
