import json


class Json:
    def __init__(self, folder: str, file: str, section: str = None):
        self.path: str = f"{folder}/{file}.json"
        self.section = section
    
    def load(self) -> dict:
        with open(self.path, "r", encoding="utf-8") as payload:
            result = json.load(payload)
            if self.section:
                return result[self.section]
            return result

    def read(self):
        with open(self.path, "r", encoding="utf-8") as payload:
            return payload.read()
                
