from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_category_services
from schemas.category import CategoryCreate, CategorySchema, CategoryUpdate
from services.category import CategoryService
from services.exceptions import NotFound

router = APIRouter(prefix='/categories')


@router.get('')
def get_categories(
    category_service: CategoryService = Depends(get_category_services)
) -> list[CategorySchema]:
    return category_service.list_category()


@router.post('', status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    category_service: CategoryService = Depends(get_category_services)
) -> CategorySchema:
    return category_service.create_category(category_crate=payload)


@router.patch('/{category_id}')
def update_category(
    category_id: str,
    payload: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_services)
):
    try:
        return category_service.update_category(
            category_id=category_id,
            category_update=payload
            )
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete(
        '/{category_id}',
        status_code=status.HTTP_204_NO_CONTENT
    )
def delete_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_services)
):
    try:
        return category_service.delete_category(category_id=category_id)
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
