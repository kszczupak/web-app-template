from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import declarative_base
from starlette.templating import Jinja2Templates

from app.config import config
# from app.core.database.table_models import User

templates = Jinja2Templates(directory=config.templates_dir)

_engine = create_engine(url=str(config.sqlalchemy_database_uri))
_Session = sessionmaker(bind=_engine)


# Create database tables on startup
# Base.metadata.create_all(bind=_engine)

def get_session():
    with _Session() as session:
        yield session


DatabaseSession = Annotated[Session, Depends(get_session)]
#
# def get_current_user(session: DatabaseSession) -> User:
#     current_user = session.get(User, ident=1)
#     assert current_user is not None
#     return current_user
#
#
# CurrentUser = Annotated[User, Depends(get_current_user)]
