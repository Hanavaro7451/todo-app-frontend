from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.category import CategoryModel


class CategoryRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> Sequence[CategoryModel]:
        return self.db.scalars(select(CategoryModel)).all()

    def get_by_id(self, category_id: str) -> CategoryModel | None:
        return self.db.get(CategoryModel, category_id)

    def create_category(self, name: str) -> CategoryModel | None:
        new_category = CategoryModel(name=name)
        self.db.add(new_category)
        self.db.commit()
        return new_category

    def delete_category(self, CategoryModel) -> None:
        self.db.delete(CategoryModel)
        self.db.commit()
