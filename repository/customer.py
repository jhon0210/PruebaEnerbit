from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas


def create(request: schemas.Customer, db: Session):
    new_customer = models.Customer(
        first_name = request.first_name,
        last_name = request.last_name,
        address = request.address,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


def get_all(db: Session):
    customers = db.query(models.Customer).all()
    return customers


def get_active(db: Session):
    customers = db.query(models.Customer).filter(models.Customer.is_active == True).all()
    return customers



def update(id, request: schemas.Customer, db: Session):
    customer = db.query(models.Customer).filter(models.Customer.id == id)

    if not customer.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'The customer width id {id} not found'
        )

    customer.update({
        'first_name': request.first_name,
        'last_name': request.last_name,
        'address': request.address,
    })

    db.commit()

    return { 'message': f'The customer was updated successfully' }


def show(id, db: Session):
    customer = db.query(models.Customer).filter(models.Customer.id == id).first()

    if not customer:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'Customer with the id {id} is not available'
        )

    return customer


def destroy(id, db: Session):
    customer = db.query(models.Customer).filter(models.Customer.id == id)

    if not customer.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'The customer width id {id} not found'
        )

    customer.delete(synchronize_session=False)
    db.commit()
    return { 'message': f'The customer {id} has been deleted sucessfully'}

