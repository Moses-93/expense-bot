from enum import Enum
from typing import Generic, TypeVar, Dict

E = TypeVar("E", bound=Enum)


class MessageProvider(Generic[E]):
    def __init__(self, messages: Dict[E, str]):
        self._messages = messages

    def get(self, key: E) -> str:
        return self._messages.get(key)
