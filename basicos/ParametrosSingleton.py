# from basicos.Singleton import Singleton
from Singleton import Singleton

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

"""
En este ejemplo:
La clase Singleton implementa el patrón Singleton, que garantiza que solo se pueda crear una única instancia de una clase.
La clase ParameterManager hereda de Singleton, lo que asegura que solo se pueda crear una instancia de ParameterManager.
La clase ParameterManager tiene métodos para establecer y obtener parámetros.
En el ejemplo de uso, creamos dos instancias de ParameterManager, pero al ser un Singleton, ambas referencian la misma 
instancia.
Configuramos un parámetro en una instancia y lo recuperamos desde la otra, lo que demuestra que ambas instancias 
comparten el mismo estado.
"""

class ParameterManager(Singleton):
    def __init__(self):
        if (super()._instance is None):         
            self.parameters = {}
            #self.parameters = self.read_config('basicos/parametros.txt')  
            self.parameters = self.read_config('emplear/basicos/parametros.txt')  

    def read_config(self, filename):
        config = {}
        with open(filename, 'r') as file:
             for line in file:                  
                 line=line.strip()                 
                 if len(line) != 0 and line[0:1] != "#":                    
                    key, value = line.strip().split("=")
                    if key not in config:  
                         config[key.strip()] = value.strip()
                    else:
                        print(f'clave: {key} repetida ... valor duplicado: {value.strip()}')
        return config 

    def set_parameter(self, key, value):
        print("seteo", key)
        self.parameters[key] = value

    def get_parameter(self, key):
        return self.parameters[key]
    
    def get_parameters(self):        
        return self.parameters

# Ejemplo de uso
if __name__ == "__main__":
    # Creamos dos instancias de ParameterManager
    param_manager1 = ParameterManager()
    
    # Configuramos un parámetro en una instancia
    param_manager1.set_parameter("language", "Python")

    # imprimimos parametros
    
    print('P M 2')    
    print(param_manager1.get_parameters())

    # Lo recuperamos desde la otra instancia
    print("Parámetro recuperado:", param_manager1.get_parameter("language"))  # Debería imprimir "Python"
