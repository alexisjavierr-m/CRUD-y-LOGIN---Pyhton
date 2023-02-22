import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

##---------------------------------------------------
#                   Coneccion
##---------------------------------------------------

server = Flask(__name__) 
server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:esteban123@34.134.216.189/CMPC'
db = SQLAlchemy(server)

df9 = pd.read_csv('Concatenado_2022.csv', delimiter=';')
df9["m/min"] = df9["tot length"]/5
df9["group name"].replace('Blocks ','Blocks',inplace=True)
stats_df9 = df9.drop(["csv-version","year","month","day","hour","min","mim-width","max-width",
              "min-thickness","max-thickn","model-name","dimensions","shift","supplier","packet ID","Product dimensions",
              "supervisor","stat length","product it","quality name",'mas class name','color','num pieces',
              'tot nominal length','tot nominal volume',"tot length",'group name','tor nominal width','toto volume','group color','-'], axis=1)

conexion = create_engine(server)
df9.to_sql(name='', con=conexion)