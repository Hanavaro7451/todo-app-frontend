import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.categories import router as category_router
from api.routers.task import router as task_router
from core.config import settings

app = FastAPI()
app.include_router(task_router)
app.include_router(category_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_methods=['*']
)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, reload=True)
