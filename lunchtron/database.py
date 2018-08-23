import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from lunchtron.settings import DATABASE

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

_LOGGER = logging.getLogger(__name__)

engine = create_engine(URL(**DATABASE), encoding='utf8', echo='debug', echo_pool=True)

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

Base = declarative_base()


def init_db():
    """Initialize our database."""
    # import lunchtron.models
    Base.metadata.create_all(engine)

    # from lunchtron.models import User
    # db_session.add_all([
    #     User(username='admin', password='fortinet'),
    #     User(username='test', password='fortinet')
    # ])
    # db_session.commit()

    _LOGGER.info('Initialized the database.')
