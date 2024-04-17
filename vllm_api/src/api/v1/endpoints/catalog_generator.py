from typing import List, Dict, Any, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from services.inference import inference_model

router = APIRouter()


class Product(BaseModel):
    product_title: str
    product_description: Optional[str] = None


class BatchInferenceRequest(BaseModel):
    products: List[Product]
    config: Dict[str, Any] = Field(default_factory=lambda: {"temperature": 0.0, "max_tokens": 300})


@router.post("/inference_product_catalog/")
async def inference_catalog(request: BatchInferenceRequest) -> JSONResponse:
    response = inference_model(request.products, request.config)
    return JSONResponse(content=response)


@router.post("/batch_inference_product_catalog/")
async def batch_inference_catalog(request_body: BatchInferenceRequest) -> JSONResponse:
    product_info = request_body.products
    config = request_body.config
    # if len(product_info) > 23:
    #     return JSONResponse(content={"error": "Maximum of 23 products are allowed per request."}, status_code=400)
    response = inference_model(product_info, config)
    return JSONResponse(content=response)