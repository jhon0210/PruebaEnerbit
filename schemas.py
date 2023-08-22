from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
from typing import List
from enum import Enum

import uuid


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    address: str


class Customer(CustomerBase):
    class Config():
        from_attributes = True


class CustomerId(BaseModel):
    id: uuid.UUID

    @validator('id')
    def validate_uuid(cls, value):
        if not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)
            except ValueError:
                raise ValueError("Invalid UUID format")
        return value


class StatusEnum(str, Enum):
    new = 'new'
    done = 'done'
    cancelled = 'cancelled'


class WorkOrderBase(BaseModel):
    id: uuid.UUID
    title: str
    planned_date_begin: datetime
    planned_date_end: datetime
    status: StatusEnum

    @validator('planned_date_end')
    def validate_time_difference(cls, planned_date_end, values, **kwargs):
        planned_date_begin = values.get('planned_date_begin')
        if planned_date_begin and planned_date_end:
            time_difference = planned_date_end - planned_date_begin
            if time_difference < timedelta(hours=2):
                raise ValueError('End time should be at least 2 hours after start time')
        return planned_date_end



class WorkOrder(WorkOrderBase):
    customer_id: uuid.UUID

    @validator('customer_id')
    def validate_uuid(cls, value):
        if not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)
            except ValueError:
                raise ValueError('Invalid UUID format')
        return value

    class Config():
        from_attributes = True


class ShowCustomer(CustomerBase):
    id: uuid.UUID
    start_date: datetime | None
    end_date: datetime | None
    is_active: bool
    created_at: datetime

    class Config():
        from_attributes = True


class ShowWorkOrder(WorkOrderBase):
    owner: ShowCustomer

    class Config():
        from_attributes = True


class ShowCustomerWorkOrderList(ShowCustomer):
    work_orders: List[WorkOrder]

    class Config():
        from_attributes = True

