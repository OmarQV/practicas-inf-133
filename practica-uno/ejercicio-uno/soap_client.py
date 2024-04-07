from zeep import Client

# Representa el cliente para el servicio web SOAP 
# que está escuchando en http://localhost:8000
client = Client('http://localhost:8000')

num1 = 8
num2 = 2
# SUMA
suma = client.service.Sumar(num1, num2)
# RESTA
resta = client.service.Restar(num1, num2)
# MULTIPLICACION
multiplicacion = client.service.Multiplicar(num1, num2)
# DIVISION
division = client.service.Dividir(num1, num2)

# SALIDA - SUMA
print("\nSUMA\n",suma)
# SALIDA - RESTA
print("\nRESTA\n",resta)
# SALIDA - MULTIPLICACION
print("\nMULTIPLICACION\n",multiplicacion)
# SALIDA - DIVISION
print("\nDIVISION\n",division)
print()