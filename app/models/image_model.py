from sqlalchemy import Column, Integer, String
from app.database.postgres import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)