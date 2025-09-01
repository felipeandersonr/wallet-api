from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, field_validator


class Message(BaseModel):
    message: str


class FilterPagination(BaseModel):
    limit: int | None = None
    offset: int | None = None


    @field_validator("limit", "offset")
    def validate_value(cls, value: int | None) -> int | None:
        if value is not None and value < 0:
            raise ValueError("limit and offset must be non-negative integers")
        
        return value


def get_filter_pagination(limit: Annotated[int | None, Query()] = None,
                          offset: Annotated[int | None, Query()] = None) -> FilterPagination:
    
    return FilterPagination(limit=limit, offset=offset)
