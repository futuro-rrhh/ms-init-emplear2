
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

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance