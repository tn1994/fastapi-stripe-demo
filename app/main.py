import logging
import traceback
from typing import Union

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.models.database import Base, SessionLocal, engine
from app.models.stripe_model import Plan, Product
from app.models.stripe_model import StripeCustomer
from app.models import crud
from app.models import schemas
from app.services.stripe_service import StripeService

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

stripe_service = StripeService()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class App:
    """
    ref: https://qiita.com/ryori0925/items/722cd64045e0142122a5
    """
    app = FastAPI()

    def __init__(self):
        origins = [
            'http://localhost:62535',
            'http://localhost:3000',
            '*',
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )

    def get_application(self):
        return self.app

    @staticmethod
    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @staticmethod
    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}

    @staticmethod
    @app.post('/products/')
    async def create_product(product: Product):
        try:
            result = stripe_service.create_product(product=product)
            return f'StripeのProduct登録に成功しました。ID: {result.get("id")}'
        except Exception:
            traceback.print_exc()
            message = "StripeのProduct登録に失敗しました"
            return message

    @staticmethod
    @app.get('/products')
    async def get_products():
        try:
            return stripe_service.get_products(limit=5)
        except Exception:
            traceback.print_exc()
            message = "StripeのProduct取得に失敗しました"
            return message

    @staticmethod
    @app.post('/plans/')
    async def create_plan(plan: Plan):
        try:
            result = stripe_service.create_plan(plan=plan)
            return f'StripeのPlan登録に成功しました。ID: {result.get("id")}'
        except Exception:
            traceback.print_exc()
            message = "StripeのPlan登録に失敗しました"
            return message

    @staticmethod
    @app.get('/plans')
    async def get_plans():
        try:
            return stripe_service.get_plans(limit=5)
        except Exception:
            traceback.print_exc()
            message = "StripeのPlan取得に失敗しました"
            return message

    @staticmethod
    @app.post("/customers/")
    async def create_customer(customer: StripeCustomer, db: Session = Depends(get_db)):
        """
        Customer Tableに存在、且つStripe側へ未登録のユーザーを登録
        """
        # DB内のCustomer検索
        try:
            crud.create_demo_customer(db=db)  # todo: delete demo create
            db_customer = crud.get_customer_by_email(
                db=db, email=customer.email)
            # todo: use this
            """
            if not db_customer:
                raise HTTPException(status_code=400, detail="Customerが存在しません")
            if db_customer.stripe_customer_id:
                raise HTTPException(
                    status_code=400,
                    detail="すでにStripeにCustomerとして登録されています")
                    """
        except Exception:
            traceback.print_exc()
            message = "StripeのCustomer登録に失敗しました"
            return message

        # Stripeへの登録
        try:
            result = stripe_service.create_customer(db_customer=db_customer)
        except Exception:
            traceback.print_exc()
            message = "StripeのCustomer登録に失敗しました"
            return message

        # StripeのCustomerIDをDBに反映
        try:
            update_customer = schemas.UpdateCustomer(
                id=db_customer.id,
                name=db_customer.name,
                email=db_customer.email,
                stripe_customer_id=result.get('id'))
            return crud.update_customer(db=db, customer=update_customer)
        except Exception:
            traceback.print_exc()
            message = "StripeのCustomer登録に失敗しました"
            return message

    @staticmethod
    @app.get("/customers")
    async def search_customers(customer: StripeCustomer = Depends(StripeCustomer)):
        try:
            result = stripe_service.search_customers(email=customer.email)
            if not result:
                raise ValueError
            return result
        except Exception:
            traceback.print_exc()
            message = "StripeのCustomer取得に失敗しました"
            return message

    @staticmethod
    @app.post("/subscriptions/")
    async def create_subscription(subscription: schemas.Subscription, db: Session = Depends(get_db)):
        """Subscription登録"""
        # DB内のCustomer検索
        db_customer = crud.get_customer_by_email(
            db, email=subscription.customer_email)
        if not db_customer:
            raise HTTPException(status_code=400, detail="Customerが存在しません")
        if db_customer.stripe_subscription_id:
            raise HTTPException(
                status_code=400,
                detail="すでにSubscriptionが登録されています")

        # Stripeへの登録
        try:
            result = stripe_service.create_subscription(
                stripe_customer_id=db_customer.stripe_subscription_id,
                subscription=subscription)
        except Exception:
            message = "StripeのSubscription登録に失敗しました"
            return message

        # StripeのSubscription IDをDBに反映
        update_customer = schemas.UpdateCustomer(
            id=db_customer.id,
            name=db_customer.name,
            email=db_customer.email,
            stripe_subscription_id=result.get('id'))

        return crud.update_customer(db=db, customer=update_customer)


app = App().get_application()
