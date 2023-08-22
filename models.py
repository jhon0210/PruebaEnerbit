from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base
import uuid
from datetime import datetime


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    work_orders = relationship('WorkOrder', back_populates='owner')


class WorkOrder(Base):
    __tablename__ = 'work_orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    title = Column(String, nullable=False)
    planned_date_begin = Column(DateTime, nullable=True)
    planned_date_end = Column(DateTime, nullable=True)
    status = Column(Enum('new', 'done', 'cancelled', name='status_enum'))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    owner = relationship('Customer', back_populates='work_orders')


