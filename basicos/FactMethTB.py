from abc import ABC, abstractmethod
from pymongo import MongoClient
from basicos.ParametrosSingleton import ParameterManager
from basicos.Errores import ErrorManager
from basicos.database import Database, DatabaseFactory

import psycopg2
import secrets

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

Parametros=ParameterManager()
Errores=ErrorManager()

# Const
const cDEBUG = Parametros.get_parameter('Debug')
const cDB = Parametros.get_parameter('UbicBD')
const cGENERAL = Parametros.get_parameter("General") 
const cLEVEL = Parametros.get_parameter('Level')

# Abstract Product
class TableConnector(ABC):
    @abstractmethod
    def execute_query(self, query, params=None):
        pass 

    def fetch_data(self, query, params=None):
        pass

    def insert_record(self, table, data):
        pass
    
    def insert_recordFull(self, table, data):
        pass

    def delete_record(self, table, condition):
        pass

    def update_record(self, table, data, condition):
        pass

# Concrete Products
class PostgresTable(TableConnector):

    def __init__(self, conn, secret):
       
        if int(cDEBUG):
            print('__init__.conn:', conn,'-secret:', secret)
        db_secret=secret
        self.conn = conn
        self.cursor=conn.cursor()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query, params)

    def fetch_data(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_record(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))


    def insert_recordFull(self, table, data):
        --columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s' for _ in data])
        query = f"INSERT INTO {table} VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))

    def delete_record(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_query(query)

    def update_record(self, table, data, condition):
        set_values = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        self.execute_query(query, tuple(data.values()))

class MongoTable(TableConnector):
    def __init__(self, conn, db_secret):
        if int(cDEBUG):
            print('__init__.conn:', conn,' - secret:', db_secret)
        self.db_secret=db_secret
        self.conn = conn
        #self.cursor=conn.cursor()
    
    def execute_query(self, query, params=None):
        pass

    def fetch_data(self, query, params=None):
        pass

    def insert_record(self, table, data):
        pass

    def delete_record(self, table, condition):
        pass

    def update_record(self, table, data, condition):
        pass

class TxtConnector(TableConnector):
    def __init__(self, config):
        self.config = config

    def connect(self):
        # client =  (self.config['host'], self.config['port'])
        db = cDB
        return db
    
    def execute_query(self, query, params=None):
        pass

    def fetch_data(self, query, params=None):
        pass

    def insert_record(self, table, data):
        pass

    def delete_record(self, table, condition):
        pass

    def update_record(self, table, data, condition):
        pass


"""
# Abstract Factory

"""
class TableFactory:
    @staticmethod
    def Link_database(database_type, conn, db_secret=None ):
        
        if database_type == "PostgreSQL":

            return PostgresTable( conn, db_secret)
        #elif database_type == "MySQL":
        #    return MySQLTable(db_secret)
        elif database_type == "MongoDB":
            if int(cDEBUG):
                print('TableFactory.link_database.conn:', conn, '-',cDEBUG,'-Fin debug')
            return MongoTable(conn, db_secret)
        #elif database_type == "TextFile":
        #    return TextFileTable(db_secret, db_File)
        else:
            raise ValueError("Unsupported database type")


# Cliente
def main():
    
    db_secret = secrets.token_urlsafe(32)
    #print("db secret:", db_secret)

    # Leer los datos de conexión desde el archivo de texto
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


"""
    data={"idUsuario":"10",
          "ctipousuario":"f", 
          "email":"prueba@gmail.com",
          "cnomyap":"Prueba Prueba", 
          "cpassword":"",
          "ctycversion":"",
          "dfechaaltaus":"","":""}

    if int(Parametros.get_parameter('Debug')):
        print(data)
    postgresTable

 
    def insert_record(self, table, data):

    def delete_record(self, table, condition):

    def update_record(self, table, data, condition):


insert into tusuarios
values (1, 'f','jcarvallo.ar@gmail.com', 'Big Cheo','123','1', '2024-04-24 00:00:00 ) 
    
    def insert_record(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))

    def delete_record(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_query(query)

    def update_record(self, table, data, condition):
        set_values = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        self.execute_query(query, tuple(data.values()))

    postgresql_db.execute_query("create table t1 (idusuario integer)", params)
    
    postgresql_db.execute_query("insert into t1 values (1) ", params)
    postgresql_db.execute_query("insert into t1 values (3) ", params)
    postgresql_db.execute_query("select * from t1 ", params)
    
    postgresql_db.execute_query("select * from tusuarios ", params)
    results=postgresTable.cursor.fetchall()
    postgresql_db.close_connection()
    for row in results:
            print('-',row,'-')
    """
    #mongo_config = read_config("mongo_config.txt")

    # Seleccionar la fábrica deseada
    # Por ejemplo, si quieres conectarte a PostgreSQL:
    # db_factory = PostgresFactory()
    # O si prefieres MongoDB:
    # db_factory = MongoFactory()

    # Crear el conector
    # Pasar la configuración correspondiente
    # db_connector = db_factory.create_connector(postgres_config)
    # db_connector = db_factory.create_connector(mongo_config)

    # Conectar a la base de datos
    # connection = db_connector.connect()
    # print("Conexión establecida:", connection)
    # print("Conexión establecida exitosamente!")
    # cursorSql=connection.cursor()
    
    #cursorSql.execute("insert into tusuarios(cTipoUsuario, eMail, cNomyAp, cPassword,ctycversion,dfechaaltaus) values ('F','gguerrataboada@gmail.com','Gabriel Guerra 2','gg','1','2024-04-24 00:00:00' )")
    #cursorSql.close
    #cursorSql=connection.cursor()
   
    

def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split("=")
            config[key.strip()] = value.strip()
    return config

if __name__ == "__main__":
    main()
