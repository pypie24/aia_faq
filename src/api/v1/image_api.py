from uuid import UUID
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Form

from src.schemas.image_schema import (
    ImageSchema,
    ImageCreateSchema,
    ImageUpdateSchema,
)
from src.services.image_services import ImageService
from src.api.v1.dependencies import get_image_service

router = APIRouter(prefix="/images", tags=["images"])


# Image Endpoints


@router.post("/", response_model=ImageSchema, status_code=status.HTTP_201_CREATED)
async def create_image(
    data: ImageCreateSchema,
    file: UploadFile = File(...),
    service: ImageService = Depends(get_image_service),
):
    return await service.create(data, file)


@router.get("/{image_id}", response_model=ImageSchema, status_code=status.HTTP_200_OK)
async def get_image(image_id: UUID, service: ImageService = Depends(get_image_service)):
    obj = await service.get(str(image_id))
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    return obj


@router.put("/{image_id}", response_model=ImageSchema, status_code=status.HTTP_200_OK)
async def update_image(
    image_id: UUID,
    data: ImageUpdateSchema,
    service: ImageService = Depends(get_image_service),
):
    obj = await service.update(str(image_id), data)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    return obj


@router.delete("/{image_id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete_image(
    image_id: UUID, service: ImageService = Depends(get_image_service)
):
    return await service.delete(str(image_id))


@router.get("/", response_model=list[ImageSchema], status_code=status.HTTP_200_OK)
async def list_images(
    skip: int = 0, limit: int = 20, service: ImageService = Depends(get_image_service)
):
    return await service.list(skip, limit)
