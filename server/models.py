from sqlalchemy import Column, String
from db import Base

class SpotifyConfigValue(Base):
    __tablename__ = 'spotify_config'
    key = Column(String, primary_key=True)
    value = Column(String)

    def __init__(self, key, value):
        self.key = key
        self.value = value
