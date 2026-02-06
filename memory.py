from typing import List


class Memory:
    def __init__(self):
        """Initialize Memory with session_id and empty messages list."""
        self._messages: List[dict] = []
    
    def add_msg(self, role, msg) -> None:
        """Add a message to the conversation chat
        
        Args:
            role: The role of the message sender (e.g., 'user', 'assistant')
            msg: The message content
        """
        self._messages.append({
            "role": role,
            "content": msg
        })
    
    def get_chat(self) -> List[dict]:
        """Return the conversation chat.
        
        Returns:
            List of message dictionaries
        """
        return self._messages
