
import json


with open("data/schema.txt", "r") as f:
    SCHEMA = f.read()


with open("data/intents.json", "r") as f:
    
    INTENTS = json.loads(f.read())