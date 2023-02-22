from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pandas as pd
import pyarrow.parquet as pq
import pandas as pd
import time

url= 'postgresql://postgres:esteban123@34.134.216.189/CMPC'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
db = SQLAlchemy(app)

# Leer el dataframe desde el archivo CSV
path = 'bd_buzones_Mulchen'
lowercase_path = path.lower()
format = '.csv'
time.sleep(1)

#df = pd.read_csv('C:/Users/Alexis Javier/Desktop/CRUD/' + path + format, sep=';', error_bad_lines=False)

# Leer el archivo CSV con PyArrow
table = pq.read_table('C:/Users/Alexis Javier/Desktop/CRUD/' + path + format, sep=';', error_bad_lines=False)

# Convertir a DataFrame de pandas
df = table.to_pandas()

columns = df.columns
lowercase_columns = [col.lower() if col.strip() != "" else col for col in columns]

# Verifica si hay nombres de columna duplicados y agrega un contador al nombre de la columna
counter = {}
new_columns = []
for col in lowercase_columns:
    if col in counter:
        counter[col] += 1
        new_column = col + '_' + str(counter[col])
    else:
        counter[col] = 0
        new_column = col
    new_columns.append(new_column)

# Reemplaza los nombres de columna en el dataframe
df.columns = new_columns

with app.app_context():
    inicio = time.time()
    df.to_sql(name=lowercase_path, con=db.engine, if_exists='replace', index=False)
    fin = time.time()

print(fin-inicio)