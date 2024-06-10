from abc import ABC, abstractmethod
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from basicos.ParametrosSingleton import ParameterManager
from basicos.Errores import ErrorManager
import secrets
import psycopg2

# from FactMethTB import TableConnector

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
const cHOST = Parametros.get_parameter("host")
const cPORT = Parametros.get_parameter("port")
const cDATABASE = Parametros.get_parameter("database")
const cUSER = Parametros.get_parameter("user")

"""
documento nacional de identidad
Una vez cerrada la versión agrego comentarios
hoy 5/5/2024 todavía falta.

"""

class Database(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def begin(self):
        pass
    
    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass

class MySQLDatabase(Database):
    def __init__(self, db_secret):
        self.db_secret = db_secret

    def connect(self):
        pass

    def begin(self):
        pass
    
    def execute_query(self, query, params=None ):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def close_connection(self):
        pass

class PostgreSQLDatabase(Database):
    def __init__(self, db_secret, config):
        self.db_secret = db_secret
        self.config = config
  
    def connect(self):
        # postgres_config = read_config("basicos/postgres_config.txt")
        connection = psycopg2.connect(**self.config)    
        if int(cDEBUG):
            print('PostgreSQLDatabase.connect.connection:', connection)
        self.cursor=connection.cursor()
        return connection
    
    # agregar manejo de error!!!!
    def begin(self):
        self.execute_query("BEGIN","")
        
    # agregar manejo de error!!!!
    def execute_query(self, query, params=None):
        if int(cDEBUG):
            print(query,'-1-',params,'')
        if params:     
            #print(query,'-2-',params,'')       
            self.cursor.execute(query, params)
        else:
            #print(query,'-3-',params,'')
            self.cursor.execute(query)
    
    # agregar manejo de error!!!!
    def commit(self):
        self.conn.commit()
        

    # agregar manejo de error!!!!
    def rollback(self):
        self.conn.rollback()

    # agregar manejo de error!!!!
    def close_connection(self):
        self.cursor.close()
        #self.conn.close()

class MongoDBDatabase(Database):
    def __init__(self, db_secret, config):
        self.db_secret = db_secret
        self.config = config
 
    def connect(self):
        client = MongoClient(self.config['host'], int(self.config['port']))
        if int(cDEBUG):
            print(self.__module__,'MongoDatabase.connect:', self.config)
        db = client[self.config['database']]
        #self.cursor=db.cursor()
        return db
        
    def begin(self):
        pass
    
    def commit(self):
        pass

    def rollback(self):
        pass

    def close_connection(self):
        pass

class TextFileDatabase(Database):
    def __init__(self, db_Secret, file_path):
        self.db_Secret= db_Secret
        self.file_path = file_path
   
    # posicion todavía no se está usando
    def write(self, dbSecret, data):
        if self.db_Secret == dbSecret: 
            with open(self.file_path, "a") as file:
                file.write(str(data) + "\n")

    def read(self, id):
        with open(self.file_path, "a") as file:
            lines = file.readlines()
            for line in lines:
                if str(id) in line:
                    print("Found in TextFile:", line.strip())

    def update(self, id, data):
        with open(self.file_path, "a") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if str(id) in line:
                    file.write(str(data) + "\n")
                else:
                    file.write(line)
            file.truncate()

    def delete(self, id):
        with open(self.file_path, "a") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if str(id) not in line:
                    file.write(line)
            file.truncate()

class DatabaseFactory:
    @staticmethod
    def get_database(database_type, db_secret=None, db_File=None ):
        config={"host":"","port":"", "database":"","user":"", "password":""}

        config["host"] = cHOST
        config["port"] = cPORT
        config["database"] = cDATABASE
        config["user"] = cUSER
        config["password"] = Parametros.get_parameter("password")
        
        if database_type == "PostgreSQL":
            return PostgreSQLDatabase(db_secret, config)
        #elif database_type == "MySQL":
        #    return MySQLDatabase(db_secret)
        elif database_type == "MongoDB":
            return MongoDBDatabase(db_secret, config)
        elif database_type == "TextFile":
            return TextFileDatabase(db_secret, db_File)
        else:
            raise ValueError("Unsupported database type")

"""
# Ejemplo de uso
if __name__ == "__main__":
    # Simulamos obtener los parámetros de conexión desde un secreto
    db_secret = secrets.token_urlsafe(16)
    print("db secret:", db_secret)
    # Obtener instancia de MySQLDatabase a través de DatabaseFactory
    #mysql_db = DatabaseFactory.get_database("MySQL", db_secret)
    #mysql_db.create({"id": 1, "name": "John"})
    # Obtener instancia de PostgreSQLDatabase a través de DatabaseFactory
    postgresql_db = DatabaseFactory.get_database("PostgreSQL", db_secret)
    conn=postgresql_db.connect()
    print(conn)
    postgresql_db.begin
    postgresql_db.execute_query("select * from tusuarios")

    results=postgresql_db.fetchall()
    postgresql_db.close
    for row in results:
            print(row)

    # Obtener instancia de MongoDBDatabase a través de DatabaseFactory
    #mongodb_db = DatabaseFactory.get_database("MongoDB", db_secret)
    #mongodb_db.delete(1)

    # Obtener instancia de TextFileDatabase a través de DatabaseFactory
    # textfile_db = DatabaseFactory.get_database("TextFile", db_secret, "database/data.txt")
    print("despues de usar Factory.")
    
    #textfile_db.write(db_secret, "3-prueba de datos.")
"""    