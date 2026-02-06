from providers import get_provider
from memory import Memory

from prompt import get_system_prompt, Response
from config import INTENTS


class Session:
    def __init__(self, session_id):

        self.session_id = session_id

        self.memory = Memory()

        self.provider = get_provider()

        self.add_message(role="system", msg=get_system_prompt())

    def get_session_chat(self) -> list[dict]:
        """
        Return the conversation chat for the session.
        following the law of demeter.
        """
        return self.memory.get_chat()

    def add_message(self, role, msg):
        """
        Add a message to the conversation chat for the session.
        following the law of demeter.
        """
        self.memory.add_msg(role=role, msg=msg)

    def call_user_message(self, msg):
        """
        Process a user message by adding it to the session chat, calling the provider, 
        and handling the response.
        """
        # call the provider and get the response
        self.add_message(role="user", msg=msg)
        response = self.provider.call(self.get_session_chat())
        ai_msg = response["content"]
        self.add_message(role="assistant", msg=ai_msg)
        resp = Response.model_validate_json(ai_msg)

        if resp.is_intent_recognized:
            # select the intent
            selected_intent = None
            for intent in INTENTS:
                if intent['intent'] == resp.intent:
                    selected_intent = intent
                    break

            query = selected_intent["sql_query"]
            answer = selected_intent["answer"]
            if resp.params:
                query = query.format(**resp.params)
                answer = answer.format(**resp.params)

            return query, answer, response["prompt_tokens"], response["completion_tokens"], response["total_tokens"]
        else:
            return "no-sql", resp.friendly_message, response["prompt_tokens"], response["completion_tokens"], response["total_tokens"]
    

if __name__ == "__main__":
    session = Session("session1")
    query, answer, prompt_tokens, completion_tokens, total_tokens = session.call_user_message("What is the total sales for the last month?")
    print("SQL Query:", query)
    print("Answer:", answer)
    print("Prompt Tokens:", prompt_tokens)
    print("Completion Tokens:", completion_tokens)
    print("Total Tokens:", total_tokens)

    print("="*20)
    query, answer, prompt_tokens, completion_tokens, total_tokens = session.call_user_message("What about last month?")
    print("SQL Query:", query)
    print("Answer:", answer)
    print("Prompt Tokens:", prompt_tokens)
    print("Completion Tokens:", completion_tokens)
    print("Total Tokens:", total_tokens)
