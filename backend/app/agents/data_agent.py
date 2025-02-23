from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

from app.services.llm_service import LLMService
from app.services.data_service import DataService
class DataAgent:
    def __init__(self):
        self.llm = LLMService()

    def analyze(self, state: dict) -> dict:
        messages = [
            ("system", '''You are a data scientist working on the data the user provided. Your task is to analyze the data and generate a report according to the user's question. You are given the user question and the relevant data in JSON string format.
                - Return the report in the following JSON format:
                    - introduction: [str] The introduction to the report.
                    - main: [str] The main content of the report.
                    - conclusion: [str] The conclusion of the report.
                    - error: [str, null] The error message if there is any issue with the question or the data.
            '''),
            ("human", '''- User question: {user_question}
                - Data: {data}
            ''')
        ]
        prompt = ChatPromptTemplate(messages)

        response = self.llm.invoke(prompt, is_response_json=True, 
                input={
                    "user_question": state.user_question,
                    "data": state.query_execute_result.get("result", "")
                }
            )
        
        if response.get("error"):
            raise ValueError(response.get("error"))
        return {
            "data_analyze_result": response
            }

    def visualize(self, state: dict) -> dict:
        messages = [
            ("system", '''You are a data scientist working on the data the user provided. Your task is to analyze the data and generate a chart according to the user's question. Choose the appropriate chart type based on the user question if the user does not specify the chart type. You are given the user question and the relevant data in JSON string format.
                - Return the report in the following JSON format:
                    - introduction: [str] The introduction to the report in text format.
                    - main: [str] The JSON string of the chart data.
                        - Format:
                            - data: [list] The data points for the chart.
                                - point: [dict] The data point. Key is the x-axis value and value is the y-axis value.
                                    - name: [str] The name of the data point.
                                    - value: [int] The value of the data point.
                            - metadata: [dict] The metadata of the chart.
                                - title: [str] The title of the chart.
                                - x_axis: [str] The label of the x-axis.
                                - y_axis: [str] The label of the y-axis.
                            - type: [str] The type of the chart. Possible values: "line", "bar", "pie", "scatter".
                    - conclusion: [str] The conclusion of the report in text format.
                    - error: [str, null] The error message if there is any issue with the question or the data.
            '''),
            ("human", '''- User question: {user_question}
                - Data: {data}
            ''')
        ]
        prompt = ChatPromptTemplate(messages)

        response = self.llm.invoke(prompt, is_response_json=True, 
                input={
                    "user_question": state.user_question,
                    "data": state.query_execute_result.get("result", "")
                }
            )
        
        if response.get("error"):
            raise ValueError(response.get("error"))
        return {
            "data_visualize_result": response
            }

    def tabulate(self, state: dict) -> dict:
        messages = [
            ("system", '''You are a data scientist working on the data the user provided. Your task is to analyze the data and generate a table according to the user's question. You are given the user question and the relevant data in JSON string format.
                - Return the report in the following JSON format:
                    - introduction: [str] The introduction to the report in text format.
                    - main: [str] The JSON string of the table data.
                        - Format:
                            - data: [list] The data points for the table.
                                - entry: [dict] The data point. Key is the entry number(starting from 0) and value is the data point.
                                    - column [str]: value [int, float, str] The data point.
                            - metadata: [dict] The metadata of the table.
                                - title: [str] The title of the table.
                                - columns: [list] The list of column names.
                    - conclusion: [str] The conclusion of the report in text format.
                    - error: [str, null] The error message if there is any issue with the question or the data.
            '''),
            ("human", '''- User question: {user_question}
                - Data: {data}
            ''')
        ]
        prompt = ChatPromptTemplate(messages)

        response = self.llm.invoke(prompt, is_response_json=True, 
                input={
                    "user_question": state.user_question,
                    "data": state.query_execute_result.get("result", "")
                }
            )
        
        if response.get("error"):
            raise ValueError(response.get("error"))
        return {
            "data_tabulate_result": response
            }
    

    def machine_learning(self, state: dict) -> dict:
        messages = [
            ("system", '''You are a data scientist working on the data the user provided. Your task is to analyze the data and generate a machine learning model according to the user's question. You are given the user question and the relevant data in JSON string format. Use the appropriate machine learning model based on the user question if the user does not specify the model. Use PythonREPL tool to run the machine learning model.
                - Return the report in the following JSON format:
                    - introduction: [str] The introduction to the report in text format.
                    - main: [str] The analysis of the results of the machine learning model invoked by you. The output should include the model's predictions, accuracy, and any other relevant information. Give the numerical results you get from the model training script.
                    - conclusion: [str] The conclusion of the report in text format.
                    - error: [str, null] The error message if there is any issue with the question or the data.
            '''),
            ("human", '''- User question: {user_question}
                - Data: {data}
            ''')
        ]
        prompt = ChatPromptTemplate(messages)

        # See https://python.langchain.com/docs/integrations/tools/python/
        python_repl = PythonREPL()
        repl_tool = Tool(
            name="PythonREPL",
            description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`. Use this tool to run the machine learning model.",
            func=python_repl.run
        )

        response = self.llm.invoke(prompt, is_response_json=True, tools=[repl_tool],
                input={
                    "user_question": state.user_question,
                    "data": state.query_execute_result.get("result", "")
                }
            )
        
        if response.get("error"):
            raise ValueError(response.get("error"))
        return {
            "data_machine_learning_result": response
            }