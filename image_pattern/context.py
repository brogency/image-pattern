from __future__ import annotations
from typing import Union, Any, TypeVar
from pydantic import BaseModel


T = TypeVar('T')


class ContextVar(BaseModel):
    key: Union[str, int]

    def get_from_context(self, context) -> Any:
        return getattr(context, self.key)


class Context(BaseModel):
    @classmethod
    def var(cls, key):
        return ContextVar(key=key)

