import requests
import json

url = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}

# Crear un paciente
print("\n---------- POST ------------")
new_patient = {
   "nombre": "Pedrito",
   "apellido": "Cuevas",
   "edad": 26,
   "genero": "M",
   "diagnostico": "Diabetes",
   "doctor": "Liliana"
}
post_response = requests.post(url, json=new_patient, headers=headers)
print(post_response.json())
print()
print("\n---------- POST ------------")
new_patient = {
   "nombre": "Maria",
   "apellido": "Vega",
   "edad": 35,
   "genero": "F",
   "diagnostico": "Hipertensión",
   "doctor": "Juan"
}
post_response = requests.post(url, json=new_patient, headers=headers)
print(post_response.json())
print()
# Listar todos los pacientes
print("---------- GET ------------")
# ruta_get_pacientes = url + "/pacientes"
get_response = requests.get(url, headers=headers)
print(get_response.json())

# Buscar pacientes por CI
print("---------- GET ------------")
get_response2 = requests.get(url + "/1", headers=headers)
print(get_response2.json())
print()
# Listar a los pacientes que tienen diagnostico de Diabetes
print("---------- GET ------------")
get_response3 = requests.get(url + "?diagnostico=Diabetes", headers=headers)
print(get_response3.json())
print()
# Listar a los pacientes que atiende el Doctor Pedro Pérez
print("---------- GET ------------")
get_response4 = requests.get(url + "?doctor=Liliana", headers=headers)
print(get_response4.json())
print()
# Actualizar la información de un paciente
print("---------- PUT ------------")
ruta_put = url + "pacientes/1002"
update_data = {
    "nombre": "Kevin",
    "edad": 60
}
put_response = requests.put(url + "/1", json=update_data, headers=headers)
print(put_response.json())
# Eliminar un paciente
print("---------- DELETE ------------")
response_delete = requests.delete(url + "/1")
print(response_delete.json())