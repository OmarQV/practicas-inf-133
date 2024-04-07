# >> pip install zeep
# >> pip install pysimplesoap
from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

# ----------- funcion -----------
# SUMAR DOS NUMEROS
def sumar(num1, num2):
   resultado = num1 + num2
   return "La suma de {} + {} es: {}".format(num1, num2, resultado)
# RESTAR DOS NUMEROS
def restar(num1, num2):
   resultado = num1 - num2
   return "La resta de {} - {} es: {}".format(num1, num2, resultado)
# MULTIPLICAR DOS NUMEROS
def multiplicar(num1, num2):
   resultado = num1 * num2
   return "La multiplicacion de {} * {} es: {}".format(num1, num2, resultado)
# DIVIDIR DOS NUMEROS
def dividir(num1, num2):
   resultado = num1 / num2
   return "La division de {} / {} es: {}".format(num1, num2, resultado)

# --------- dispatcher ---------
# ----- conexion --------
dispatcher = SoapDispatcher(
   "ejercicio1-soap-server",                 # Nombre del dispatcher
   location="http://localhost:8000/",     # URL del servidor SOAP
   action="http://localhost:8000/",       # Acción SOAP
   namespace="http://localhost:8000/",    # Espacio de nombres
   trace=True,                            # Habilita el seguimiento de mensajes SOAP
   ns=True                                # Habilita el manejo de espacios de nombres SOAP
)
# SUMAR DOS NUMEROS
# Registrar -- funciones --
dispatcher.register_function(
   "Sumar",                               # Nombre del método de servicio SOAP
   sumar,                                 # Función o método que implementa la operación de suma
   returns = {"sumar": str},              # Especifica el tipo de dato devuelto por el método de servicio
   args = {"num1": int, "num2": int}      # Especifica los argumentos de entrada del método de servicio
)
# RESTAR DOS NUMEROS
dispatcher.register_function(
   "Restar",                              # Nombre del método de servicio SOAP
   restar,                                # Función o método que implementa la operación de suma
   returns = {"restar": str},             # Especifica el tipo de dato devuelto por el método de servicio
   args = {"num1": int, "num2": int}      # Especifica los argumentos de entrada del método de servicio
)
# MULTIPLICAR DOS NUMEROS
dispatcher.register_function(
   "Multiplicar",                         # Nombre del método de servicio SOAP
   multiplicar,                           # Función o método que implementa la operación de suma
   returns = {"multiplicar": str},        # Especifica el tipo de dato devuelto por el método de servicio
   args = {"num1": int, "num2": int}      # Especifica los argumentos de entrada del método de servicio
)
# DIVIDIR DOS NUMEROS
dispatcher.register_function(
   "Dividir",                             # Nombre del método de servicio SOAP
   dividir,                               # Función o método que implementa la operación de suma
   returns = {"dividir": str},            # Especifica el tipo de dato devuelto por el método de servicio
   args = {"num1": int, "num2": int}      # Especifica los argumentos de entrada del método de servicio
)

def run():
   try:
      server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
      server.dispatcher = dispatcher
      print("Iniciando servidor SOAP en http://localhost/8000/")
      server.serve_forever()
   except KeyboardInterrupt:
      print("Apagando servidor SOAP...")
      server.socket.close()
      
if __name__ == "__main__":
   run()
   