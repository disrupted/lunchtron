from sqlalchemy import Column, String, Integer, Numeric

from lunchtron.database import Base


class User(Base):
    __tablename__ = 'users'

    user_uid = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    price = Column(Numeric(6, 2))
    balance = Column(Numeric(6, 2))

    def __init__(self, name=None, price=None, balance=None):
        self.name = name
        self.price = price
        self.balance = balance

    def __repr__(self):
        return "<User(user_uid=%d, username='%s', price='%s', balance='%s')>" % (
            self.user_uid, self.name, self.price, self.balance)

    def to_dict(self):
        return {
            'user_uid': self.user_uid,
            'username': self.name,
            'price': self.price,
            'balance': self.balance
        }
