from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from services.tag_services import TagService, TagAssignmentService
from src.schemas.tag_schema import (
    TagSchema,
    TagCreateSchema,
    TagUpdateSchema,
    TagAssignmentSchema,
    TagAssignmentCreateSchema,
    TagAssignmentUpdateSchema,
)
from src.api.v1.dependencies import get_tag_service, get_tag_assignment_service

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagSchema, status_code=status.HTTP_201_CREATED)
async def create_tag(
    data: TagCreateSchema, service: TagService = Depends(get_tag_service)
):
    return await service.create(data)


@router.get("/{tag_id}", response_model=TagSchema, status_code=status.HTTP_200_OK)
async def get_tag(tag_id: UUID, service: TagService = Depends(get_tag_service)):
    obj = await service.get(str(tag_id))
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return obj


@router.put("/{tag_id}", response_model=TagSchema, status_code=status.HTTP_200_OK)
async def update_tag(
    tag_id: UUID, data: TagUpdateSchema, service: TagService = Depends(get_tag_service)
):
    obj = await service.update(str(tag_id), data)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return obj


@router.delete("/{tag_id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete_tag(tag_id: UUID, service: TagService = Depends(get_tag_service)):
    return await service.delete(str(tag_id))


@router.get("/", response_model=list[TagSchema], status_code=status.HTTP_200_OK)
async def list_tags(
    skip: int = 0, limit: int = 20, service: TagService = Depends(get_tag_service)
):
    return await service.list(skip, limit)


@router.post(
    "/{tag_id}/assignments",
    response_model=TagAssignmentSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag_assignment(
    tag_id: UUID,
    data: TagAssignmentCreateSchema,
    service: TagAssignmentService = Depends(get_tag_assignment_service),
):
    return await service.create(tag_id, data)


@router.get(
    "/{tag_id}/assignments/{assignment_id}",
    response_model=TagAssignmentSchema,
    status_code=status.HTTP_200_OK,
)
async def get_tag_assignment(
    tag_id: UUID,
    assignment_id: UUID,
    service: TagAssignmentService = Depends(get_tag_assignment_service),
):
    obj = await service.get(str(assignment_id))
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TagAssignment not found"
        )
    return obj


@router.put(
    "/{tag_id}/assignments/{assignment_id}",
    response_model=TagAssignmentSchema,
    status_code=status.HTTP_200_OK,
)
async def update_tag_assignment(
    tag_id: UUID,
    assignment_id: UUID,
    data: TagAssignmentUpdateSchema,
    service: TagAssignmentService = Depends(get_tag_assignment_service),
):
    obj = await service.update(str(assignment_id), data)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TagAssignment not found"
        )
    return obj


@router.delete(
    "/{tag_id}/assignments/{assignment_id}",
    response_model=bool,
    status_code=status.HTTP_200_OK,
)
async def delete_tag_assignment(
    tag_id: UUID,
    assignment_id: UUID,
    service: TagAssignmentService = Depends(get_tag_assignment_service),
):
    return await service.delete(str(assignment_id))


@router.get(
    "/{tag_id}/assignments",
    response_model=list[TagAssignmentSchema],
    status_code=status.HTTP_200_OK,
)
async def list_tag_assignments(
    tag_id: UUID,
    skip: int = 0,
    limit: int = 20,
    service: TagAssignmentService = Depends(get_tag_assignment_service),
):
    return await service.list(tag_id, skip, limit)
