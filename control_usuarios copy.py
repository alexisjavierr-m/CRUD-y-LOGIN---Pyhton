import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State, ALL, MATCH

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
    html.H1('Capacity Dashboard', className='text-center my-4'),
    html.P('Agregar Roles'),
    dbc.Row([
        dbc.Col([
            dbc.Input(id='input-nombre', type='text', value='', placeholder='Ingresar ROL')
        ], width=4),
        dbc.Col([
            dbc.Button('Agregar', id='button-submit', color='primary'),
            html.Div(id='output-message')
        ], width=2)
    ], className='my-4'),
    html.H3('Roles Existentes'),
    dbc.Row([
        dbc.Col([
            dbc.Button('Mostrar Roles', id='boton-mostrar', color='primary'),
            html.Div(id='datos-mostrados')
        ], width=6)
    ], className='my-4'),
    html.Hr(),
    html.P('Agregar Areas'),
    dbc.Row([
        dbc.Col([
            dbc.Input(id='input-nombre2', type='text', value='', placeholder='Ingresar Area')
        ], width=4),
        dbc.Col([
            dbc.Button('Agregar', id='button-submit2', color='primary'),
            html.Div(id='output-message2')
        ], width=2)
    ], className='my-4'),
    html.H3('Areas Existentes'),
    dbc.Row([
        dbc.Col([
            dbc.Button('Mostrar Areas', id='boton-mostrar2', color='primary'),
            html.Div(id='datos-mostrados2')
        ], width=6)
    ], className='my-4'),
    html.Hr(),
    html.H3('Usuarios'),
    dbc.Row([
        dbc.Col([
            dbc.Button('Mostrar Usuarios', id='boton-mostrar4', color='primary'),
            html.Div(id='datos-mostrados4')
        ], width=6)
    ], className='my-4')
], fluid=True)

##---------------------------------------------------
#                   Mostrar USUARIOS
##---------------------------------------------------

@app.callback(
    Output("datos-mostrados4", "children"),
    [
        Input("boton-mostrar4", "n_clicks")
    ],
)

def register_usuario(n_clicks):
    if n_clicks is not None:
        a = db.session.query(Usuario).all()
        lista_usuario_id = [row.id for row in a]
        lista_usuario_name = [row.name for row in a]
        lista_usuario_email = [row.email for row in a]
        lista_usuario_rol_id = [row.rol_id for row in a]
        lista_usuario_area_id = [row.area_id for row in a]
        roles = db.session.query(Rol).all()
        opciones_rol = [{"label": r.nombre, "value": r.id} for r in roles]

        areas = db.session.query(Area).all()
        opciones_area = [{"label": a.nombre, "value": a.id} for a in areas]

        rows = []
        for i in range(len(a)):
            row = [
                html.Td(lista_usuario_name[i],style={'width': '25%'}),
                html.Td(lista_usuario_email[i],style={'width': '25%'}),
                html.Td(
                    dcc.Dropdown(
                        options=opciones_rol,
                        value=lista_usuario_rol_id[i],
                        id={"type": "rol-dropdown", "index": i},
                    ), style={'width': '25%'}
                ),
                html.Td(
                    dcc.Dropdown(
                        options=opciones_area,
                        value=lista_usuario_area_id[i],
                        id={"type": "area-dropdown", "index": i},
                    ), style={'width': '25%'}
                ),
            ]
            rows.append(html.Tr(row))

        table_header = [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Name"),
                        html.Th("Email"),
                        html.Th("Rol"),
                        html.Th("Area"),
                    ]
                )
            )
        ]
        table_body = [html.Tbody(rows)]
        return dbc.Table(table_header + table_body, bordered=True)
    else:
        return ""

##---------------------------------------------------
#                   ACTUALIZAR USUARIOS
##---------------------------------------------------

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

def register_area(n_clicks):
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
#            Arranque de Aplicación
##---------------------------------------------------

with server.app_context():
    db.create_all()
    # server.run()
    app.run_server(debug=True)
