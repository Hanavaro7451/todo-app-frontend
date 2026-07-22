from sqlalchemy.orm import Mapped

from models.base import Base


class CategoryModel(Base):
    __tablename__ = 'categories'
    name: Mapped[str]
