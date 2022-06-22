# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from apps import db, login_manager
from apps.authentication.util import hash_pass
class RawMaterial(db.Model):

    __tablename__ = 'RawMaterial'

    number=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    def test_schema(self):
        return {
            'name': self.name,
            'number': self.number,
            'description': self.description,
        }



class RawMaterialDetail(db.Model):

    __tablename__ = 'RawMaterialDetail'

    id = db.Column(db.String(64), primary_key=True)
    number=db.Column(db.Integer)
    status=db.Column(db.BOOLEAN)



    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)

class Product(db.Model):
    __tablename__ = 'Product'

    number=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    technology =db.Column(db.String(64))
    description =db.Column(db.String(256))

    def __repr__(self):
        return str(self.number)
    def test_schema(self):
        return {
            'name': self.name,
            'number': self.number,
            'description': self.description,
            'technology':self.technology,
        }

class Order(db.Model):
    __tablename__ = 'Order'

    number=db.Column(db.Integer,)
    name = db.Column(db.String(64),primary_key=True)
    description =db.Column(db.String(256))
    ordered=db.Column(db.String(16),)

    def __repr__(self):
        return str(self.number)
    def test_schema(self):
        return {
            'name': self.name,
            'number': self.number,
            'description': self.description,
            'ordered':self.ordered,
        }


class PathDetail(db.Model):
    __tablename__ = 'PathDetail'


    bom=db.Column(db.String(256))
    path=db.Column(db.String(64),primary_key=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.path)
    def test_schema(self):
        return {
            'bom': self.bom,
            'path': self.path,
        }


class WorkStation(db.Model):
    __tablename__ = 'WorkStation'
    name=db.Column(db.String(64))
    number=db.Column(db.Integer,primary_key=True)
    IP=db.Column(db.String(15))
    kind=db.Column(db.String(64))
    production_line=db.Column(db.String(64))


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.number)


class Device(db.Model):
    __tablename__ = 'Device'
    name=db.Column(db.String(64))
    number=db.Column(db.Integer,primary_key=True)
    work_station_number=db.Column(db.Integer)
    operation=db.Column(db.String(256))


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.number)