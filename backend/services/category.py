from sqlalchemy.orm import Session

from repositories.categories import CategoryRepository
from schemas.category import CategoryCreate, CategorySchema, CategoryUpdate
from services.exceptions import NotFound


class CategoryService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repo = CategoryRepository(db)

    def list_category(self) -> list[CategorySchema]:
        categories = self.category_repo.get_all()
        return [
            CategorySchema.model_validate(category) for category in categories
        ]

    def create_category(
        self,
        category_crate: CategoryCreate
    ) -> CategorySchema:
        category = self.category_repo.create_category(name=category_crate.name)
        self.db.commit()
        return CategorySchema.model_validate(category)

    def update_category(
        self,
        category_id: str,
        category_update: CategoryUpdate
    ) -> CategorySchema:
        category_for_update = self.category_repo.get_by_id(
            category_id=category_id)
        if category_for_update is None:
            raise NotFound('Категория не найдена')
        if category_update.name:
            category_for_update.name = category_update.name
        self.db.commit()
        return CategorySchema.model_validate(category_for_update)

    def delete_category(self, category_id: str) -> None:
        category_for_delete = self.category_repo.get_by_id(category_id)
        if category_for_delete is None:
            raise NotFound('Категория не найдена')
        self.category_repo.delete_category(category_for_delete)
