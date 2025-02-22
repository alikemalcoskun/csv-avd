import pandas as pd
import pandasql as ps
import json



class DataService:
    def __init__(self):
        self.data = None
    
    def from_df(self, data):
        self.data = data
        return self
    
    def from_json(self, data):
        self.data = pd.read_json(data)
        return self
    
    def from_json_str(self, data):
        return self.from_json(json.loads(data))

    def from_csv_file(self, data_path):
        self.data = pd.read_csv(data_path)
        return self
    
    def to_json(self):
        return self.data.to_json()
    
    def to_json_str(self):
        return json.dumps(self.to_json())
    
    def get_schema(self):
        return self.data.dtypes.to_dict()
    
    def get_head(self):
        return self.data.head().to_dict()
    
    def execute_query(self, query):
        data = self.data
        try:
            return {
                "result": ps.sqldf(query, locals()).to_json(),
                "error": None
            }
        except Exception as e:
            return {
                "result": None,
                "error": str(e)
            }
