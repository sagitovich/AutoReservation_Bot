from sqlalchemy import VARCHAR, BigInteger, Column, sql

from db.db_gino import BaseModel


class Forms(BaseModel):
    __tablename__ = 'forms'
    form_id = Column(BigInteger, primary_key=True)
    truck = Column(VARCHAR)
    trailer = Column(VARCHAR)
    trans_type = Column(VARCHAR)
    trans_species = Column(VARCHAR)
    special_cargo = Column(VARCHAR)
    date = Column(VARCHAR)
    query: sql.select


class Trucks(BaseModel):
    __tablename__ = 'trucks'
    truck = Column(VARCHAR, primary_key=True)
    date = Column(VARCHAR)
    status = Column(VARCHAR)
    query: sql.select
