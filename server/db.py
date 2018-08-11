from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
Session = None

class SpotifyConfigValue(Base):
    __tablename__ = 'spotify_config'
    key = Column(String, primary_key=True)
    value = Column(String)

    def __init__(self, key, value):
        self.key = key
        self.value = value

# init the db engine
def init_db():
    engine = create_engine('sqlite:///db.db', echo=True)
    Base.metadata.create_all(engine)
    global Session
    Session = sessionmaker(bind=engine)

def get_session():
    return Session()
