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

class Bypass_usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

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
    html.H3('Tabla de Roles'),
    dbc.Row([
        dbc.Col([
            dbc.Input(id='input-nombre', type='text', value='', placeholder='Ingresar ROL')
        ], width=4),
        dbc.Col([
            dbc.Button('Agregar', id='button-submit', color='primary'),
            html.Div(id='output-message')
        ], width=2),
        dbc.Col([
            dbc.Button('Mostrar Roles', id='boton-mostrar', color='primary'),
        ], width=2)
    ], className='my-4'),
    dbc.Row([
        dbc.Col([
            html.Div(id='datos-mostrados')
        ], width=4)
    ], className='my-4'),
    html.Hr(),
    html.H3('Tabla de Areas'),
    dbc.Row([
        dbc.Col([
            dbc.Input(id='input-nombre2', type='text', value='', placeholder='Ingresar Area')
        ], width=4),
        dbc.Col([
            dbc.Button('Agregar', id='button-submit2', color='primary'),
            html.Div(id='output-message2')
        ], width=2),
        dbc.Col([
            dbc.Button('Mostrar Areas', id='boton-mostrar2', color='primary'),
        ], width=2)
    ], className='my-4'),
    dbc.Row([
        dbc.Col([
            html.Div(id='datos-mostrados2')
        ], width=4)
    ], className='my-4'),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.H3('Asignación de Usuarios'),
        ], width=2),
        dbc.Col([
            dbc.Button('Mostrar Usuarios', id='boton-mostrar4', color='primary'),
        ], width=4)
    ], className='my-4'),
    dbc.Row([
        dbc.Col([
            html.Div(id='datos-mostrados4')
        ], width=8)
    ], className='my-4'),
    html.Hr(),
    html.H3('Tabla Correos Permitidos'),
    dbc.Row([
        dbc.Col([
            dbc.Input(id='input-nombre-correo', type='text', value='', placeholder='Ingresar Correo')
        ], width=4),
        dbc.Col([
            dbc.Button('Agregar', id='button-submit-correo', color='primary'),
            html.Div(id='output-message-correo')
        ], width=2),
        dbc.Col([
            dbc.Button('Mostrar Correos', id='boton-mostrar-correos', color='primary'),
        ], width=4)
    ], className='my-4'),
        
    dbc.Row([
        dbc.Col([
            html.Div(id='datos-mostrados-correos')
        ], width=4)
    ], className='my-4'),
], fluid=True)

##---------------------------------------------------
#                   Mostrar CORREO-BYPASS
##---------------------------------------------------
@app.callback(
    Output("datos-mostrados-correos", "children"),
    [
        Input("boton-mostrar-correos", "n_clicks")
    ],
)

def register_Bypass_usuario(n_clicks):
    if n_clicks is not None:
        a = db.session.query(Bypass_usuario).all()
        lista_bypass_usuario_id = [row.id for row in a]
        lista_bypass_usuario_email = [row.email for row in a]
#       dict_Bypass_usuario = {"Correo Ingresados": lista_bypass_usuario_email}
#       df = pd.DataFrame(dict_Bypass_usuario)
#       return make_table(df)

        rows = []
        for i in range(len(a)):
            row = [
                html.Td(lista_bypass_usuario_email[i],style={'width': '25%'}),
                 html.Td(
                    dbc.Col([
                        dbc.Button('Eliminar', id={"type": "eliminar-button", "index": lista_bypass_usuario_id[i]}, color='danger'),
                        html.Div(id={"type": "eliminar-output", "index": lista_bypass_usuario_id[i]})
                    ]),
                ),
            ]
            rows.append(html.Tr(row))

        table_header = [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Correo"),
                    ]
                )
            )
        ]
        table_body = [html.Tbody(rows)]
        return dbc.Table(table_header + table_body, bordered=True)
    else:
        return ""

##---------------------------------------------------
#                   Eliminar CORREO-BYPASS
##---------------------------------------------------

@app.callback(
    Output({"type": "eliminar-output", "index": MATCH}, "children"),
    Input({"type": "eliminar-button", "index": MATCH}, "n_clicks"),
    State({"type": "eliminar-button", "index": MATCH}, "id"),
)
def delete_Bypass_usuario(n_clicks, button_id):

    if n_clicks:
        # Obtenemos el índice del usuario que estamos actualizando
        index = button_id["index"]
        print(f"Index: {index}")  # Agregar mensaje de depuración
        # Obtenemos el usuario correspondiente al índice
        db.session.query(Bypass_usuario).filter_by(id=index).delete()
        # Guardamos los cambios en la base de datos
        db.session.commit()
        return "Correo Eliminado correctamente"
    else:
        return ''

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
                        id={"type": "rol-dropdown", "index": lista_usuario_id[i]},
                    ), style={'width': '25%'}
                ),
                html.Td(
                    dcc.Dropdown(
                        options=opciones_area,
                        value=lista_usuario_area_id[i],
                        id={"type": "area-dropdown", "index": lista_usuario_id[i]},
                    ), style={'width': '25%'}
                ),
                 html.Td(
                    dbc.Col([
                        dbc.Button('Guardar', id={"type": "guardar-button", "index": lista_usuario_id[i]}, color='primary'),
                        html.Div(id={"type": "guardar-output", "index": lista_usuario_id[i]})
                    ]),
                ),
            ]
            rows.append(html.Tr(row))

        table_header = [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Nombre"),
                        html.Th("Correo"),
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

@app.callback(
    Output({"type": "guardar-output", "index": MATCH}, "children"),
    Input({"type": "guardar-button", "index": MATCH}, "n_clicks"),
    State({"type": "rol-dropdown", "index": MATCH}, "value"),
    State({"type": "area-dropdown", "index": MATCH}, "value"),
    State({"type": "guardar-button", "index": MATCH}, "id"),
)
def actualizar_usuario(n_clicks, rol_id, area_id, button_id):

    if n_clicks:
        # Obtenemos el índice del usuario que estamos actualizando
        index = button_id["index"]
        print(f"Index: {index}")  # Agregar mensaje de depuración
        # Obtenemos el usuario correspondiente al índice
        usuario = db.session.query(Usuario).filter_by(id=index).first()
        if usuario is not None:  # Verificamos si se obtuvo un usuario válido
            # Actualizamos los datos del usuario
            usuario.rol_id = rol_id
            usuario.area_id = area_id
            # Guardamos los cambios en la base de datos
            db.session.commit()
            return "Usuario actualizado correctamente"
        else:
            return "No se encontró el usuario"
    else:
        return ""

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
#                   AGREGA CORREO
##---------------------------------------------------

@app.callback(
    Output("output-message-correo", "children"),
    [
        Input("button-submit-correo", "n_clicks")
    ],
    [
        State("input-nombre-correo", "value")
    ]
)

def register_area(n_clicks, value):
    if n_clicks is not None:
        a = db.session.execute(db.select(Bypass_usuario))
        bypass_usuario = Bypass_usuario(email=value)
        db.session.add(bypass_usuario)
        db.session.commit()
        return f"Correo {value} registrado correctamente"
    else:
        return ''

##---------------------------------------------------
#            Arranque de Aplicación
##---------------------------------------------------

with server.app_context():
    db.create_all()
    # server.run()
    app.run_server(debug=True)
