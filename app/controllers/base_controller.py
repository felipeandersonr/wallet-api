from sqlalchemy.orm import Session


class BaseController:
    def __init__(self, session: Session):
        self.session = session
