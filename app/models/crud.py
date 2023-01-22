from sqlalchemy.orm import Session

from . import schemas

"""about sqlalchemy
https://qiita.com/arkuchy/items/75799665acd09520bed2
"""


def create_demo_customer(db: Session):
    demo_user = schemas.Customer(
        name='hoge',
        email='hoge@example.co.jp',
        # stripe_customer_id='demo_customer_id',
        # stripe_subscription_id='demo_subscription_id'
    )
    db.add(demo_user)
    db.commit()
    return demo_user


def get_customer_by_email(db: Session, email: str):
    return db.query(schemas.Customer).filter(
        schemas.Customer.email == email).first()


def update_customer(db: Session, customer: schemas.UpdateCustomer):
    """
    https://coffee-blue-mountain.com/https-coffee-blue-mountain-com-python-flask-sqlalchemy-orm-record-update/
    """
    db_item = db.query(schemas.UpdateCustomer).filter(
        schemas.UpdateCustomer.id == customer.id).one()
    db_item.update_dict(customer)
    db.add(db_item)
    db.commit()
    return db_item
