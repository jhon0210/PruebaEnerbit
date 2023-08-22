from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import redis

from .. import models, schemas


redis_host = 'localhost'
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def create(request: schemas.WorkOrder, is_active: bool, db: Session):
    total_work_orders = db.query(models.WorkOrder).filter(
        models.WorkOrder.customer_id == request.customer_id
    ).count()

    if total_work_orders > 0:
        customer = db.query(models.Customer).filter(
            models.Customer.id == request.customer_id
        )

        if customer.first().is_active and is_active == False:
            customer.update({
                'is_active': is_active,
                'end_date': datetime.now()
            })

    new_order = models.WorkOrder(
        customer_id = request.customer_id,
        title = request.title,
        planned_date_begin = request.planned_date_begin,
        planned_date_end = request.planned_date_end,
        status = 'new',
    )

    db.add(new_order) 
    db.commit()
    db.refresh(new_order)

    return new_order


def get_all(db: Session):
    orders = db.query(models.WorkOrder).all()
    return orders


def get_all_from_range(since, until, status, db: Session):
    if status == None:
        filtered_orders = db.query(models.WorkOrder).filter(
            models.WorkOrder.created_at.between(since, until)
        ).all()
    else:
        filtered_orders = db.query(models.WorkOrder).filter(
            models.WorkOrder.created_at.between(since, until),
            models.WorkOrder.status == status
        ).all()

    return filtered_orders


def update(id, request: schemas.WorkOrder, db: Session):
    order = db.query(models.WorkOrder).filter(models.WorkOrder.id == id)

    if not order.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'The order width id {id} not found'
        )

    order.update({
        'first_name': request.first_name,
        'last_name': request.last_name,
        'address': request.address,
    })

    db.commit()

    return { 'message': f'The order was updated successfully' }


def finish(id, db: Session):
    order = db.query(models.WorkOrder).filter(models.WorkOrder.id == id)

    if not order.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'The order width id {id} not found'
        )

    total_ended_orders = db.query(models.WorkOrder).filter(
        models.WorkOrder.customer_id == order.first().customer_id,
        models.WorkOrder.status == 'done').count()

    if total_ended_orders == 0:
        customer = db.query(models.Customer).filter(models.Customer.id == order.first().customer_id)
        customer.update({
            'is_active': True,
            'start_date': datetime.now() 
        })

    order.update({ 'status': 'done' })

    db.commit()

    stream_key = 'work_orders_done'

    event_data = {
        'id': str(order.first().id),
        'customer_id': str(order.first().customer_id),
        'title': order.first().title,
        'planned_date_begin': str(order.first().planned_date_begin),
        'planned_date_end': str(order.first().planned_date_end),
        'status': str(order.first().status),
        'created_at': str(order.first().created_at),
    }

    event_id = redis_client.xadd(stream_key, event_data)
    print(event_id)

    return { 'message': f'The order was updated successfully' }



def show(id, db: Session):
    order = db.query(models.WorkOrder).filter(models.WorkOrder.id == id).first()

    if not order:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'Order with the id {id} is not available'
        )

    return order


def destroy(id, db: Session):
    order = db.query(models.WorkOrder).filter(models.WorkOrder.id == id)

    if not order.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'The order width id {id} not found'
        )

    order.delete(synchronize_session=False)
    db.commit()
    return { 'message': f'The order {id} has been deleted sucessfully'}

