import sqlalchemy as sa

import savalidation.validators as val
from sqlalchemybwp import db
from sqlalchemybwp.lib.declarative import declarative_base
from sqlalchemybwp.lib.decorators import ignore_unique, transaction

Base = declarative_base(metadata=db.meta)

class Widget(Base):
    __tablename__ = 'cbwptestapp_widgets'

    widget_type = sa.Column(sa.Unicode(255), nullable=False)
    color = sa.Column(sa.Unicode(255), nullable=False)
    quantity = sa.Column(sa.Integer, nullable=False)

    val.validates_constraints()