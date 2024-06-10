from abc import ABC, abstractmethod
from pymongo import MongoClient
import psycopg2

class DatabaseConnector(ABC):
    @abstractmethod
    def connect(self):
        pass

# Concrete Products
class PostgresConnector(DatabaseConnector):
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        return connection

class MongoConnector(DatabaseConnector):
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database

    def connect(self):
        client = MongoClient(f'mongodb://{self.host}:{self.port}/')
        db = client[self.database]
        return db
