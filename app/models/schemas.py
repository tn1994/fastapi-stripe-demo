from pydantic import BaseModel
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from .database import Base


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    stripe_customer_id = Column(String(255))
    stripe_subscription_id = Column(String(255))


class UpdateCustomer(Customer):
    email: str

    def update_dict(self, update_items: Customer):
        _update_items = {
            'id': update_items.id,
            'name': update_items.name,
            'email': update_items.email,
            'stripe_customer_id': update_items.stripe_customer_id,
            'stripe_subscription_id': update_items.stripe_subscription_id,
        }
        for name, value in _update_items.items():
            if name in self.__dict__:
                setattr(self, name, value)


class Subscription(BaseModel):
    customer_email: str
    plan: str
    quantity: int
    billing_cycle_anchor: str
    backdate_start_date: str
