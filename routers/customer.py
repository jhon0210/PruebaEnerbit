from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import database, schemas, models
from ..repository import customer


router = APIRouter(
    prefix='/customers',
    tags=['Customers']
)

get_db = database.get_db


@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemas.Customer, db: Session = Depends(get_db)):
    return customer.create(request, db)


@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Customer, db: Session = Depends(get_db)):
    return customer.update(id, request, db)


@router.get('/', response_model=List[schemas.ShowCustomerWorkOrderList])
def get_all(db: Session = Depends(get_db)):
    return customer.get_all(db)


@router.get('/active')
def get_active(db: Session = Depends(get_db)):
    return customer.get_active(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowCustomer)
def show(id, response: Response, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == id).first()

    if not customer:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'Customer with the id {id} is not available'
        )

    return customer


@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == id)

    if not customer.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'The customer width id {id} not found'
        )

    customer.delete(synchronize_session=False)
    db.commit()
    return { 'message': f'The customer {id} has been deleted sucessfully'}

