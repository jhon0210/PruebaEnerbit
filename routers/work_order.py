from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, Response, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from .. import database, schemas, models
from ..repository import work_order


router = APIRouter(
    prefix='/work_orders',
    tags=['Work Orders']
)

get_db = database.get_db


@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemas.WorkOrder, is_active: bool, db: Session = Depends(get_db)):
    return work_order.create(request, is_active, db)


@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id, request: schemas.WorkOrder, db: Session = Depends(get_db)):
    return work_order.update(id, request, db)


@router.put('/{id}/status/done', status_code = status.HTTP_202_ACCEPTED)
def set_done(id, db: Session = Depends(get_db)):
    return work_order.finish(id, db)


@router.get('/', response_model=List[schemas.ShowWorkOrder])
def get_all(db: Session = Depends(get_db)):
    return work_order.get_all(db)


@router.get('/{since}/{until}/{status}')
def get_all_from_range(since: datetime, until: datetime, status: str | None, db: Session = Depends(get_db)):
    return work_order.get_all_from_range(since, until, status, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowWorkOrder)
def show(id, response: Response, db: Session = Depends(get_db)):
    order = db.query(models.WorkOrder).filter(models.WorkOrder.id == id).first()

    if not order:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'Order with the id {id} is not available'
        )

    return order


@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    order = db.query(models.WorkOrder).filter(models.WorkOrder.id == id)

    if not order.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'The order width id {id} not found'
        )

    order.delete(synchronize_session=False)
    db.commit()
    return { 'message': f'The order {id} has been deleted sucessfully'}

