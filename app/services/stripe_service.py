import os
import datetime
from typing import Final

import stripe

from ..models.schemas import Subscription, Customer
from ..models.stripe_model import Product, Plan

"""ref
https://stripe.com/docs/api?lang=python
https://qiita.com/ryori0925/items/722cd64045e0142122a5
"""


class StripeServiceBase:
    stripe = stripe
    stripe.api_key = os.environ['STRIPE_SECRET_KEY']

    def convert_to_unixtime(dt: str):
        unixtime = int(
            datetime.datetime.strptime(
                dt, "%Y-%m-%d %H:%M:%S %z").timestamp())
        return unixtime


class StripeProduct(StripeServiceBase):
    def create_product(self, product: Product):
        return self.stripe.Product.create(
            name=product.name
            # name=product.name,
            # active=product.active,
            # description=product.description,
            # metadata=product.metadata
        )

    def get_products(self, limit: int = 5):
        return self.stripe.Product.list(limit=limit)


class StripePlan(StripeServiceBase):
    CURRENCY: Final[str] = 'jpy'

    BASIC_PLAN = {
        # todo: setup
    }
    PRO_PLAN = {
        # todo: setup
    }

    def create_plan(self, plan: Plan):
        return self.stripe.Plan.create(
            amount=plan.amount,  # 1単位当たりの金額
            currency=self.CURRENCY,  # 通貨単位(今回はJPY固定)
            interval=plan.interval,  # 支払の周期。1ヶ月毎なら"month"など
            product=plan.product,  # 商品のID
            nickname=plan.nickname  # プランの名前
        )

    def get_plans(self, limit: int = 5):
        """
        https://stripe.com/docs/api/plans/list?lang=python#list_plans
        """
        return self.stripe.Plan.list(limit=limit)


class StripeCustomer(StripeServiceBase):

    def create_customer(self, db_customer: Customer):
        return self.stripe.Customer.create(
            name=db_customer.name,
            email=db_customer.email
        )

    def search_customers(self, email: str):
        """
        https://stripe.com/docs/api/customers/search?lang=python
        """
        if not isinstance(email, str):
            raise TypeError
        if '@' not in email:
            raise ValueError
        if not email.endswith('@example.co.jp'):
            raise ValueError  # todo: this is debug code

        result = self.stripe.Customer.search(
            query=f'email:"{email}"',
        )
        if not result:
            return False
        return result


class StripeSubscription(StripeServiceBase):

    def create_subscription(
            self,
            stripe_customer_id: str,
            subscription: Subscription):
        return self.stripe.Subscription.create(
            customer=stripe_customer_id,
            items=[{"plan": subscription.plan, "quantity": subscription.quantity}],
            collection_method="send_invoice",
            days_until_due=30,
            billing_cycle_anchor=self.convert_to_unixtime(dt=subscription.billing_cycle_anchor),
            proration_behavior="create_prorations",
            backdate_start_date=self.convert_to_unixtime(dt=subscription.backdate_start_date)
        )


class StripeService(
        StripeProduct,
        StripePlan,
        StripeCustomer,
        StripeSubscription):
    pass
