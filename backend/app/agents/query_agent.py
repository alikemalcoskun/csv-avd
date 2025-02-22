from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_service import LLMService, LLMServiceMock
from app.services.data_service import DataService

class QueryAgent:
    def __init__(self):
        self.llm = LLMService()

    def generate(self, state: dict) -> dict:
        messages = [
            ("system", '''You are a data scientist working on the data the user provided.
                You are responsible for generating an SQL query that will help you extract the data according to the user's question from the Pandas DataFrame.
                You are given the the user question and the DataFrame schema.
                
                It is important to consider the following:
                - The user question might be about reports, charts, or any other data analysis of a subset of the data. I will consider any type of analysis later.
                You are responsible for generating the SQL query to get the subset of the data only.

                If the question is not clear, relative to the data, or any other issue, fill the "error" field with the issue message, else fill with null.

                Some examples of the user questions, the schema, and the expected output:
                - User question: "Who is the youngest person in the data?"
                - DataFrame schema: "id: int, name: str, age: int"
                - Expected output: "SELECT * FROM data ORDER BY age ASC LIMIT 1"

                - User question: "What is the time interval with the most sales?"
                - DataFrame schema: "id: int, date: date, sales: int, buyer: str, product: str, price: float"
                - Expected output: "SELECT * FROM data GROUP BY date ORDER BY sales DESC LIMIT 1"

                The output format you should provide:
                - query: [str] The SQL query that will help you extract the data according to the user's question.
                - error: [str, null] The error message if there is any issue with the question or the data.
            '''),
            ("human", '''
                - User question: {user_question}
                - DataFrame schema: {data_schema}
                - DataFrame head: {data_head}
            ''')
        ]
        # Add SQL query execution error if any
        if state.query_execute_result == "fail":
            sql_query_error_message = ("system", f'''
                The SQL query '{state.query_generate_result.get("query", "")}' failed to execute with the error: {state.query_execute_result.get("error", "")}
                Please also consider this error while generating the SQL query.
            ''')

            # Add before human message
            messages.insert(1, sql_query_error_message)

        prompt = ChatPromptTemplate(messages)

        data = DataService().from_json_str(state.data)
        data_schema = data.get_schema()
        data_head = data.get_head()
        response = self.llm.invoke(prompt, is_response_json=True, 
                input={
                    "user_question": state.user_question,
                    "data_schema": data_schema,
                    "data_head": data_head
                }
            )

        if response.get("error"):
            raise ValueError(response.get("error"))

        return {
            "query_generate_result": response
        }

    def execute(self, state: dict) -> dict:
        data = DataService().from_json_str(state.data)
        query = state.query_generate_result.get("query", "")

        query_result = data.execute_query(query)
        return {
            "query_execute_result": query_result
        }