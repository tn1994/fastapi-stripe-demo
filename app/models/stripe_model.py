from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    active: Optional[bool] = True
    description: Optional[str] = ''
    metadata: Optional[dict] = {}


class Plan(BaseModel):
    amount: int
    interval: str
    product: str
    nickname: Optional[str] = None


class StripeCustomer(BaseModel):
    email: str


class CustomerBase(BaseModel):
    id: int
    name: str
    email: str
    stripe_customer_id: str
    stripe_subscription_id: str
