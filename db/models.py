from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship

from connection import session

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50))
    registration_date = Column(Date)
    credits = relationship('Credits', back_populates='user')

    @classmethod
    def exists_users(cls) -> ["User"]:
        users = session.query(User).all()
        return users

    @classmethod
    def get(cls, user_id: int) -> "User":
        user = session.query(cls).filter(cls.id == user_id).first()
        return user


class Credits(Base):
    __tablename__ = 'credits'
    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    user = relationship('User', back_populates='credits')

    issuance_date = Column(Date)
    return_date = Column(Date)
    actual_return_date = Column(Date, nullable=True)
    body = Column(' body', Integer)
    percent = Column(Integer)  # в бд умножена на 100 для учета копеек

    payments = relationship('Payments', back_populates='credit')

    @classmethod
    def get_sum_by_date(cls, first_day:datetime.date, date: datetime.date) -> int:
        total_sum = session.query(func.sum(cls.body))
        total_sum = total_sum.filter(cls.issuance_date.between(first_day, date)).scalar()
        return total_sum

    @classmethod
    def get_quantity_by_month(cls, month: int, year: int) -> int:
        credit_count_for_month = session.query(func.count(cls.id)).filter(
            func.YEAR(cls.issuance_date) == year,
            func.MONTH(cls.issuance_date) == month
        ).scalar()
        return credit_count_for_month

    @classmethod
    def get_sum_by_month(cls, month: int, year: int) -> int:
        credit_sum_for_month = session.query(func.sum(cls.body)).filter(
            func.YEAR(cls.issuance_date) == year,
            func.MONTH(cls.issuance_date) == month
        ).scalar()
        return credit_sum_for_month

    @classmethod
    def get_sum_by_year(cls, year: int) -> int:
        credit_sum_for_year = session.query(func.sum(cls.body)).filter(
            func.YEAR(cls.issuance_date) == year
        ).scalar()
        return credit_sum_for_year


class Dictionary(Base):
    __tablename__ = 'dictionaries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

    plans = relationship('Plans', back_populates='category')
    payments = relationship('Payments', back_populates='type')

    @classmethod
    def get_id_by_name(cls, name: str) -> int:
        dictionary = session.query(cls).filter(cls.name == name).one()
        return dictionary.id


class Plans(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(Date)
    sum = Column(Integer)

    category_id = Column(Integer, ForeignKey("dictionaries.id", ondelete='CASCADE'))
    category = relationship('Dictionary', back_populates='plans')

    @classmethod
    def check_if_exists(cls, period: str, category_id: int) -> bool:
        plan = session.query(cls).filter(cls.period == period, cls.category_id == category_id).first()
        return True if plan else False

    @classmethod
    def get_first(cls):
        plan = session.query(cls).first()
        return plan

    @classmethod
    def get_all_by_period(cls, period: datetime.date) -> list["Plans"]:
        plans = session.query(cls).filter(cls.period == period).all()
        return plans

    @classmethod
    def get_by_category_and_month(cls, month: int, year: int, category_id: int) -> "Plans":
        plans = session.query(cls).filter(
            func.YEAR(cls.period) == year,
            func.MONTH(cls.period) == month,
            cls.category_id == category_id
        ).first()
        return plans


class Payments(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sum = Column(Integer)  # в бд умножена на 100 для учета копеек
    payment_date = Column(Date)
    credit_id = Column(Integer, ForeignKey("credits.id", ondelete='CASCADE'))
    credit = relationship('Credits', back_populates='payments')
    type_id = Column(Integer, ForeignKey("dictionaries.id", ondelete='CASCADE'))
    type = relationship('Dictionary', back_populates='payments')

    @classmethod
    def get_sum_by_credit(cls, credit_id: int, type: str) -> int:
        type_id = Dictionary.get_id_by_name(type)
        total_sum = session.query(func.sum(cls.sum))
        total_sum = total_sum.filter(cls.credit_id == credit_id, cls.type_id == type_id).scalar()
        return total_sum

    @classmethod
    def get_sum_by_date(cls, first_day:datetime.date, date: datetime.date) -> int:
        total_sum = session.query(func.sum(cls.sum)).filter(cls.payment_date.between(first_day, date)).scalar()
        return total_sum

    @classmethod
    def get_quantity_by_month(cls, month: int, year: int) -> int:
        payments_count_for_month = session.query(func.count(cls.id)).filter(
            func.YEAR(cls.payment_date) == year,
            func.MONTH(cls.payment_date) == month
        ).scalar()
        return payments_count_for_month

    @classmethod
    def get_sum_by_month(cls, month: int, year: int) -> int:
        payments_sum_for_month = session.query(func.sum(cls.sum)).filter(
            func.YEAR(cls.payment_date) == year,
            func.MONTH(cls.payment_date) == month
        ).scalar()
        return payments_sum_for_month

    @classmethod
    def get_sum_by_year(cls, year:int) -> int:
        payments_sum_for_year = session.query(func.sum(cls.sum)).filter(
            func.YEAR(cls.payment_date) == year
        ).scalar()
        return payments_sum_for_year
