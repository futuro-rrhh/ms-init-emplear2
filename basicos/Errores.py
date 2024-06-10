# from basicos.ParametrosSingleton import ParameterManager
from ParametrosSingleton import ParameterManager

from datetime import datetime

Parametros=ParameterManager()

"""
En el bloque except, se manejan diferentes tipos de excepciones de manera específica, y se utiliza ErrorManager para 
registrar el mensaje de error.
Se proporciona un ejemplo de uso donde se instancia ErrorManager y se manejan errores específicos, registrando los 
mensajes de error correspondientes.
Este es solo un ejemplo básico y se puede extender según tus necesidades específicas, como agregar funcionalidades 
adicionales para manejar diferentes tipos de errores, enviar notificaciones, etc.
"""
#Se define una clase ErrorManager que tiene un método handle_error para manejar y registrar errores. 
class ErrorManager:
    
    def __init__(self, log_file=Parametros.get_parameter('ErrorLog')):
        self.log_file = log_file

    #El método handle_error abre un archivo de registro y escribe el mensaje recibido como parámetro en el archivo.
    def handle_error(self, secret, error_message):
        try:
            # Abrir el archivo de registro en modo de escritura, agregando al final
            print(self.log_file)
            with open(self.log_file, "a") as file:
                now = datetime.now()
                # Escribir el mensaje de error en el archivo de registro               
                file.write("secret:" + secret + "-" + error_message + "-" + now.strftime("%d/%m/%Y %H:%M:%S")  + "\n")
            
            print("Error:", self.log_file, "- Fecha y Hora:", now, secret)
        except Exception as e:
            # Si ocurre algún error al intentar escribir en el archivo de registro, imprimir el error en la consola
            print("Error al registrar el error:", str(e))

# Ejemplo de uso
if __name__ == "__main__":
    # Crear una instancia de ErrorManager
    error_manager = ErrorManager()
    secret = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        # Código donde podrían ocurrir errores
        resultado = 10 / 0
        print("El resultado es:", resultado)

    except ZeroDivisionError as e:
        # Manejar el error y registrar el mensaje de error utilizando ErrorManager
        error_manager.handle_error(secret, "Error: No se puede dividir por cero")

    except Exception as e:
        # Manejar cualquier otra excepción y registrar el mensaje de error utilizando ErrorManager
        error_manager.handle_error(secret, "Error: " + str(e))

