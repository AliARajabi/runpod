from fastapi import APIRouter
from starlette.status import HTTP_404_NOT_FOUND
from api.v1.endpoints.catalog_generator import router as catalog_generator_router
from api.v1.endpoints.health import router as health

router = APIRouter()

router.include_router(catalog_generator_router,
                      responses={HTTP_404_NOT_FOUND: {"description": "Not found"}})

router.include_router(health,
                      responses={HTTP_404_NOT_FOUND: {"description": "Not found"}})
