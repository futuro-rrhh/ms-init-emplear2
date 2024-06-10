from abc import ABC, abstractmethod
from pymongo import MongoClient
from basicos.ParametrosSingleton import ParameterManager
from basicos.Errores import ErrorManager
from database import Database, DatabaseFactory
from basicos.FactMethTB import TableConnector, TableFactory
import psycopg2
import secrets

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

Parametros=ParameterManager()
Errores=ErrorManager()
TbConn=TableConnector() 
TbFact=TableFactory()

# TB  Structure
#    prueba de comentario
#    def execute_query(self, query, params=None):
#    def fetch_data(self, query, params=None):
#    def insert_record(self, table, data):
#    def insert_recordFull(self, table, data):
#    def delete_record(self, table, condition):
#    def update_record(self, table, data, condition):

# Const
const cDEBUG = Parametros.get_parameter('Debug')
const cDB = Parametros.get_parameter('UbicBD')
const cGENERAL = Parametros.get_parameter("General") 
const cLEVEL = Parametros.get_parameter('Level')
const cBOGeneral = Parametros.get_parameter('BOGeneral')

Persona = {
    "idPersona": 0,
    "dsPersona": "",
    "ctipopersona": "F",  # Fisica o Juridica
    "email": "",
    "dfecvalidmail": ,
    "cnombrepers":"",
    "capellidopers":"",
    "cpassword":"",
    "ctycversion":"",
    "dfecaltpers":,
    "bfecmodpers":,
    "bbuscatalento": False,
    "bbuscatrabajo": False,
    "idpaisalta": ,
    "idpaisnac": ,
    "idpaisdoc": ,
    "iddociden": ,
    "nrodociden": ,
    "fnacpersona": 
}

# 
class BOPersona():

    def __init__(self):
       
        if int(cDEBUG):
            print('bopersona.__init__:')
        
    def LoadPersona(self, pidPersona)
        pass
    
    def SetdsPersona( pdsPersona):
        Persona["dsPersona"]=pdsPersona

    def AltaPersona():
        pass

def main():
    
    db_secret = secrets.token_urlsafe(32)
    #print("db secret:", db_secret)

    bd=DatabaseFactory()
    ConnDb = bd.get_database(Parametros.get_parameter("General"), db_secret)
    conn=ConnDb.connect()
    if int(Parametros.get_parameter('Debug')):
        print (db_secret)
    Table= TableFactory.Link_database(cGENERAL, conn , db_secret )
    if int(cDEBUG):
        print('main.conn:', conn)
    Table.execute_query("select * from tusuarios")
    
    #results=Table.cursor.fetchall()
    if int(cLEVEL):
        for row in results:
            print('-',row,'-')
