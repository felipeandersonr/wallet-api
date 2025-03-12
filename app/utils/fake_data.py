import random

from typing import Type
from faker import Faker
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import T


faker_data = Faker()


def get_random_nonexistent_id(session: Session, model_class: Type[T]) -> int:
    statement = select(func.max(model_class.id))
    result = session.execute(statement)

    last_id = result.scalar() or 0
    random_id = last_id + random.randint(1, 1000)
    
    while session.get(model_class, random_id) is not None:
        random_id = last_id + random.randint(1, 1000)
    
    return random_id
