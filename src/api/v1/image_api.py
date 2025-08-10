from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.image_schema import (
    ImageSchema,
    ImageCreateSchema,
    ImageUpdateSchema,
    ImageAssignmentSchema,
    ImageAssignmentCreateSchema,
    ImageAssignmentUpdateSchema,
)
from src.services.image_services import ImageService, ImageAssignmentService
from src.api.v1.dependencies import get_image_service, get_image_assignment_service

router = APIRouter(prefix="/images", tags=["images"])


# Image Endpoints


@router.post("/", response_model=ImageSchema, status_code=status.HTTP_201_CREATED)
async def create_image(
    data: ImageCreateSchema, service: ImageService = Depends(get_image_service)
):
    return await service.create(data)


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


# ImageAssignment Endpoints


@router.post(
    "/{image_id}/assignments",
    response_model=ImageAssignmentSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_image_assignment(
    image_id: UUID,
    data: ImageAssignmentCreateSchema,
    service: ImageAssignmentService = Depends(get_image_assignment_service),
):
    return await service.create(image_id, data)


@router.get(
    "/{image_id}/assignments/{assignment_id}",
    response_model=ImageAssignmentSchema,
    status_code=status.HTTP_200_OK,
)
async def get_image_assignment(
    image_id: UUID,
    assignment_id: UUID,
    service: ImageAssignmentService = Depends(get_image_assignment_service),
):
    obj = await service.get(str(assignment_id))
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ImageAssignment not found"
        )
    return obj


@router.put(
    "/{image_id}/assignments/{assignment_id}",
    response_model=ImageAssignmentSchema,
    status_code=status.HTTP_200_OK,
)
async def update_image_assignment(
    image_id: UUID,
    assignment_id: UUID,
    data: ImageAssignmentUpdateSchema,
    service: ImageAssignmentService = Depends(get_image_assignment_service),
):
    obj = await service.update(str(assignment_id), data)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ImageAssignment not found"
        )
    return obj


@router.delete(
    "/{image_id}/assignments/{assignment_id}",
    response_model=bool,
    status_code=status.HTTP_200_OK,
)
async def delete_image_assignment(
    image_id: UUID,
    assignment_id: UUID,
    service: ImageAssignmentService = Depends(get_image_assignment_service),
):
    return await service.delete(str(assignment_id))


@router.get(
    "/{image_id}/assignments",
    response_model=list[ImageAssignmentSchema],
    status_code=status.HTTP_200_OK,
)
async def list_image_assignments(
    image_id: UUID,
    skip: int = 0,
    limit: int = 20,
    service: ImageAssignmentService = Depends(get_image_assignment_service),
):
    return await service.list(image_id, skip, limit)
