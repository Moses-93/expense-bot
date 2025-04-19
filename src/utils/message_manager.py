from typing import Tuple, Dict


class MessageManager:
    def __init__(self, messages: Dict):
        self.messages = messages

    def get(self, *keys, default=""):
        for key in keys:
            result = self.messages.get(key, {})
        return result if isinstance(result, str) else default

    def get_step_message(self, field: str) -> Tuple[str, str]:
        step_data = self.messages.get("steps", {}).get(field, {})
        return (
            step_data.get("text", ""),
            step_data.get("skip_callback", ""),
        )
