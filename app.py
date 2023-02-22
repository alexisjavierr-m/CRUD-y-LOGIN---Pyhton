from flask_sqlalchemy import SQLAlchemy
from models import Rol, db

db = SQLAlchemy()

def create_rol(nombre):
    rol = Rol(nombre=nombre)
    db.session.add(rol)
    db.session.commit()
    return f"Rol {nombre} creado correctamente."

def get_all_roles():
    roles = Rol.query.all()
    return roles

def get_rol_by_name(nombre):
    rol = Rol.query.filter_by(nombre=nombre).first()
    return rol

def delete_rol(nombre):
    rol = Rol.query.filter_by(nombre=nombre).first()
    db.session.delete(rol)
    db.session.commit()
    return f"Rol {nombre} eliminado correctamente."