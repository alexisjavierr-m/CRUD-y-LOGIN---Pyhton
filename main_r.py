import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

# Importar Flask y Flask-SQLAlchemy
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

##---------------------------------------------------
#                   Coneccion
##---------------------------------------------------

server = Flask(__name__) 
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:esteban123@34.134.216.189/CMPC'
db = SQLAlchemy(server)

##---------------------------------------------------
#             Modelamiento de BD
##---------------------------------------------------

#class Usuario(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #nombre = db.Column(db.String(80), unique=True, nullable=False)
    #rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=True)
    # def __repr__(self):
    #     return '<Usuario %r>' % self.nombre

#class Rol(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  nombre = db.Column(db.String(80), unique=False, nullable=False)
   # usuarios = db.relationship('Usuario', backref='rol', lazy=True)
    # def __repr__(self):
    #     return '<Rol %r>' % self.nombre

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(1000), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=True)

class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=False, nullable=False)
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=False, nullable=False)
    usuarios = db.relationship('Usuario', backref='area', lazy=True)

def make_table(dataframe):
    return dbc.Table.from_dataframe(
        dataframe, bordered=True, hover=True, responsive=True, striped=True, style={}
    )

##---------------------------------------------------
#                   HTML
##---------------------------------------------------

app.layout = dbc.Container([

    dbc.Row(dbc.Col(html.H2("Agregar Roles"))),    
    dbc.Row([
        dbc.Col(html.P("Nuevo Rol:")),
    ]),
    dbc.Row([
        dbc.Col(dbc.Input(id="input-nombre", type="text", value="")),
    ]),
    dbc.Row(dbc.Col(dbc.Button("Agregar", id="button-submit"))),
    dbc.Row(dbc.Col(html.Div(id="output-message"))),
    
    dbc.Row(dbc.Col(dbc.Button("Mostrar ROLES", id="boton-mostrar"))),
    dbc.Row(dbc.Col(html.Div(id="datos-mostrados"))),

    dbc.Row(dbc.Col(html.H2("Agregar Areas"))),    
    dbc.Row([
        dbc.Col(html.P("Nuevo Area:")),
    ]),
    dbc.Row([
        dbc.Col(dbc.Input(id="input-nombre2", type="text", value="")),
    ]),
    dbc.Row(dbc.Col(dbc.Button("Agregar", id="button-submit2"))),
    dbc.Row(dbc.Col(html.Div(id="output-message2"))),

    dbc.Row(dbc.Col(dbc.Button("Mostrar AREAS", id="boton-mostrar2"))),
    dbc.Row(dbc.Col(html.Div(id="datos-mostrados2"))),  
    
    dbc.Row([
        dbc.Col(html.P("Seleccione rol a actualizar:")), 
    ]),
    dbc.Row([
        dbc.Col(dbc.Select(id="options-id", options=[], value=None)),
    ]),
    dbc.Row([
        dbc.Col(html.P("Nuevo nombre:")),
    ]),
    dbc.Row([
        dbc.Col(dbc.Input(id="input-nombre-update", type="text", value="")),
    ]),
    dbc.Row(dbc.Col(dbc.Button("Actualizar", id="button-update"))),
    dbc.Row(dbc.Col(html.Div(id="output-message-update"))),
    dbc.Row(dbc.Col(dbc.Button("Eliminar", id="button-delete"))),
    dbc.Row(dbc.Col(html.Div(id="output-message3"))),
], fluid=True)

@app.callback(
    Output("options-id", "options"),
    [
        Input("button-submit", "n_clicks")
    ],
)

def register_rol(s):
    # a = db.session.execute(db.select(Usuario.nombre)).scalars()
    a = db.session.query(Rol).all()
    # users = db.select(Rol)
    # a = Rol.query.all()
    lista_rol = [row.id for row in a]
    return lista_rol

##---------------------------------------------------
#                   Mostrar ROLES
##---------------------------------------------------
@app.callback(
    Output("datos-mostrados", "children"),
    [
        Input("boton-mostrar", "n_clicks")
    ],
)

def register_rol(n_clicks):
    if n_clicks is not None:
        a = db.session.query(Rol).all()
        lista_rol_id = [row.id for row in a]
        lista_rol_nombre = [row.nombre for row in a]
        dict_rol = {"id": lista_rol_id, "nombre": lista_rol_nombre}
        df = pd.DataFrame(dict_rol)
        return make_table(df)
    else:
        return ''

##---------------------------------------------------
#                   Mostrar AREAS
##---------------------------------------------------
@app.callback(
    Output("datos-mostrados2", "children"),
    [
        Input("boton-mostrar2", "n_clicks")
    ],
)

def register_rol(n_clicks):
    if n_clicks is not None:
        a = db.session.query(Area).all()
        lista_area_id = [row.id for row in a]
        lista_area_nombre = [row.nombre for row in a]
        dict_area = {"id": lista_area_id, "nombre": lista_area_nombre}
        df = pd.DataFrame(dict_area)
        return make_table(df)
    else:
        return ''

##---------------------------------------------------
#                   AGREGA ROL
##---------------------------------------------------
@app.callback(
    Output("output-message", "children"),
    [
        Input("button-submit", "n_clicks")
    ],
    [
        State("input-nombre", "value")
    ]
)

def register_rol(n_clicks, value):
    if n_clicks is not None:
        a = db.session.execute(db.select(Rol))
        rol = Rol(nombre=value)
        db.session.add(rol)
        db.session.commit()
        return f"Rol {value} registrado correctamente"
    else:
        return ''

##---------------------------------------------------
#                   AGREGA AREA
##---------------------------------------------------
@app.callback(
    Output("output-message2", "children"),
    [
        Input("button-submit2", "n_clicks")
    ],
    [
        State("input-nombre2", "value")
    ]
)

def register_area(n_clicks, value):
    if n_clicks is not None:
        a = db.session.execute(db.select(Area))
        area = Area(nombre=value)
        db.session.add(area)
        db.session.commit()
        return f"Area {value} registrada correctamente"
    else:
        return ''

##---------------------------------------------------
#                   Elimina
#---------------------------------------------------
@app.callback(
    Output("output-message3", "children"),
    [Input("button-delete", "n_clicks")],
    [State("options-id", "value")],
)

def eliminar_rol(n_clicks, value):
    print(value)
    if n_clicks is None:
        return 'Seleccione un rol y haga clic en el botón "Eliminar"'

    rol = Rol.query.filter_by(id=value).first()
    db.session.delete(rol)
    db.session.commit()
    
    return "Rol eliminado exitosamente"

##---------------------------------------------------
#                   Actualiza
#---------------------------------------------------
@app.callback(
    Output("output-message-update", "children"),
    [
        Input("button-update", "n_clicks")
    ],
    [
        State("options-id", "value"),
        State("input-nombre-update", "value")
    ]
)
def update_rol(n_clicks, id_rol, nombre):
    if n_clicks is not None:
        rol = Rol.query.filter_by(id=id_rol).first()
        if rol is None:
            return "Rol no encontrado"
        else:
            rol.nombre = nombre
            db.session.commit()
            return "Rol actualizado exitosamente"
    else:
        return "Presione el botón 'Actualizar' para actualizar un rol"

##---------------------------------------------------
#            Arranque de Aplicación
##---------------------------------------------------

with server.app_context():
    db.create_all()
    # server.run()
    app.run_server(debug=True)
