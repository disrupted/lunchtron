import datetime

from sqlalchemy import Column, String, Integer, Numeric, DateTime

from lunchtron.database import Base


class Admin(Base):
    __tablename__ = 'admins'

    username = Column(String(50), primary_key=True, unique=True)
    password_hash = Column(String(100))

    def __init__(self, username=None, password_hash=None):
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return "<User(username='%s', password_hash='%s')>" % (
            self.username, self.password_hash)

    def to_dict(self):
        return {
            'username': self.username,
            'password_hash': self.password_hash
        }


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    price = Column(Numeric(6, 2))
    balance = Column(Numeric(6, 2))

    def __init__(self, name=None, price=None, balance=None):
        self.name = name
        self.price = price
        self.balance = balance

    def __repr__(self):
        return "<User(id=%d, name='%s', price='%s', balance='%s')>" % (
            self.id, self.name, self.price, self.balance)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'balance': self.balance
        }


class Card(Base):
    __tablename__ = 'cards'

    card_uid = Column(String(8), primary_key=True, unique=True)
    user_uid = Column(Integer)

    def __init__(self, user_uid=None):
        self.user_uid = user_uid

    def __repr__(self):
        return "<User(card_uid='%s', user_uid=%d)>" % (
            self.card_uid, self.user_uid)

    def to_dict(self):
        return {
            'card_uid': self.card_uid,
            'user_uid': self.user_uid
        }


class Checkin(Base):
    __tablename__ = 'checkins'

    checkin_uid = Column(Integer, primary_key=True)
    user_uid = Column(Integer)
    when = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user_uid=None, when=None):
        self.user_uid = user_uid,
        self.when = when

    def __repr__(self):
        return "<User(checkin_uid='%s', user_uid=%d, when='%s')>" % (
            self.checkin_uid, self.user_uid, self.when)

    def to_dict(self):
        return {
            'checkin_uid': self.checkin_uid,
            'user_uid': self.user_uid,
            'when': self.when
        }
