import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request, url_for
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from googleapiclient.discovery import build
import urllib.request
import csv
from sqlalchemy.exc import OperationalError, DatabaseError


# Importar Flask y Flask-SQLAlchemy
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# Configurar la aplicación Flask
server = Flask(__name__)
server.config.update(SECRET_KEY=os.urandom(12))
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.secret_key = "d.com"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

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

GOOGLE_CLIENT_ID = "255780652998-r4v78bffn9vmlf0cfmt7a52kjpibqbsi.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:8050/callback"
)

# Crear una lista vacía para almacenar los emails
ALLOWED_EMAILS = []

# Decorador para proteger una ruta
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper

# Ruta para el inicio de sesión con Google
@server.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


# Ruta para la callback del inicio de sesión con Google
@server.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # Verificar si el correo electrónico está permitido
    name = id_info.get("name")
    email = id_info.get("email")
    image_url = id_info.get("picture")
    
    if email not in ALLOWED_EMAILS:
        return "Solo los usuarios con correo electrónico válido pueden acceder a esta página."  # Acceso no autorizado

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email") 
    session["image_url"] = image_url
        
    # Obtener la imagen de perfil del usuario
    people_service = build('people', 'v1', credentials=credentials)
    person = people_service.people().get(resourceName='people/me', personFields='photos').execute()
    photos = person.get('photos', [])
    if len(photos) > 0:
        session['image_url'] = photos[0]['url']
    
    user = Usuario.query.filter_by(email=email).first()
    if user:
        return redirect('/protected_area')
    else:
        # User does not exist, add to database
        new_user = Usuario(name=name, email=email, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/protected_area')

# Ruta para el cierre de sesión
@server.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# Ruta para la página principal
@server.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"


# Ruta para el área protegida
@server.route("/protected_area")
@login_is_required
def protected_area():
            return f"Hola, {session['name']},{session['email']},<img style='border-radius: 50px;' src='{session['image_url']}' width='50' height='50'</img><br/><a href='/logout'><button>Logout</button></a>"

#--------------------
app.layout = html.Div([
    html.H1("Hola cristian"),
    html.Br(),
    html.A(dbc.Button(id='google-login', type='submit', children='Login with Google', style={'background-color': '#4285F4', 'color': 'white', 'border': 'none', 'padding': '8px 16px', 'text-align': 'center', 'text-decoration': 'none', 'display': 'inline-block', 'font-size': '16px', 'border-radius': '5px'}), href='/login'),
    html.Br(),
    html.Div(id='protected-area', children=[])
])


@app.callback(
    Output('protected-area', 'children'),
    Input('google-login', 'n_clicks')
)
def update_protected_area(n_clicks):
    if n_clicks is not None:
        if "google_id" not in session:
            return dcc.Location(pathname='/login', id='login-redirect')
        else:
            return f"Hello {session['name']},{session['email']},<img style='border-radius: 50px;' src='{session['image_url']}' width='50' height='50 </img><br/><a href='/logout'><button>Logout</button></a>"

def get_data():
    # Intentar conectarse a la base de datos
    database_available = True
    if database_available:
        with server.app_context():
            db.create_all()
            Bypass_usuarios = Bypass_usuario.query.all()
            ALLOWED_EMAILS = [Bypass_usuario.email for Bypass_usuario in Bypass_usuarios]

        # Guardar los datos descargados en un archivo CSV local
        with open('data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for email in ALLOWED_EMAILS:
                writer.writerow([email])
    else:
        # Si la base de datos no está disponible, cargar los datos directamente desde el archivo CSV
        if os.path.exists('data.csv'):
            with open('data.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                ALLOWED_EMAILS = [row[0] for row in reader]
        else:
            ALLOWED_EMAILS = []

# Devolver los datos cargados desde la base de datos o desde el archivo CSV
    return ALLOWED_EMAILS

with server.app_context():
    # server.run()
    ALLOWED_EMAILS = get_data()
    print(ALLOWED_EMAILS)
    app.run_server(debug=True)

#with server.app_context():
#    db.create_all()
#    Iterar sobre cada objeto y agregar su email a la lista
#    Bypass_usuarios = Bypass_usuario.query.all()
#    for Bypass_usuario in Bypass_usuarios:
#        ALLOWED_EMAILS.append(Bypass_usuario.email)