from pydantic import BaseModel, Field
from typing import Optional

from config import SCHEMA, INTENTS
from datetime import datetime


class Response(BaseModel):
    is_intent_recognized: bool = Field(..., description="Whether the intent was recognized or not")
    friendly_message: Optional[str] = Field(..., description="A friendly message to the user if the intent was not recognized")
    
    intent: Optional[str] = Field(..., description="The recognized intent")
    params: Optional[dict] = Field(..., description="The parameters of the recognized intent if any")


intent_desc = ("\n"+("="*10)+"\n").join([f"""
- intent_name: {intent['intent']} 

- params: {', '.join(intent['params'] if intent['params'] != {} else ['none'])}

- summary: {intent['summary']}""" for intent in INTENTS])


def get_system_prompt() -> str:
    """
    Generate the system prompt for the AI model based on the schema, intents, and current date/time.
    """

    system_prompt = f"""
    You are a helpful assistant Your task is to understand the user's intent
    and choose the correct intent from the list of available intents
    given the database schema and the user chat.

    **CURRENT DATE AND TIME** : {str(datetime.now())}

    **AVAILABLE INTENTS** :

    {intent_desc}  

    **SCHEMA** : 
                
    {SCHEMA}


    FOLLOW THIS FORMAT IN YOUR RESPONSE:

    {Response.model_json_schema()}

    Rules:
    - Use double quotes for all keys and strings.
    - Use true/false for booleans.
    - Use null for None.
    - Do not include extra text or explanations if intent is recognized.

    """
    return system_prompt