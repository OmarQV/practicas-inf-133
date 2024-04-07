import requests

url = "http://localhost:8000/"

# Crear un paciente
print("\n---------- POST ------------")
ruta_post = url + "pacientes"
new_patient = {
   "ci": 1003,
   "nombre": "Pedrito",
   "apellido": "Cuevas",
   "edad": 26,
   "genero": "M",
   "diagnostico": "Diabetes",
   "doctor": "Liliana"
}
post_response = requests.post(ruta_post, json=new_patient)
print(post_response.text)
print()

# Listar todos los pacientes
print("---------- GET ------------")
ruta_get_pacientes = url + "/pacientes"
get_response = requests.get(ruta_get_pacientes)
print(get_response.text)

# Buscar pacientes por CI
print("---------- GET ------------")
ci = 1001
ruta_get_ci = url + f"pacientes/{ci}"
get_response2 = requests.get(ruta_get_ci)
print(get_response2.text)
print()
# Listar a los pacientes que tienen diagnostico de Diabetes
print("---------- GET ------------")
diagnostico = "Diabetes"
ruta_get_diagnostico = url + f"pacientes?diagnostico={diagnostico}"
get_response3 = requests.get(ruta_get_diagnostico)
print(get_response3.text)
print()
# Listar a los pacientes que atiende el Doctor Pedro Pérez
print("---------- GET ------------")
doctor = "Liliana"
ruta_get_doctor = url + f"pacientes?doctor={doctor}"
get_response4 = requests.get(ruta_get_doctor)
print(get_response4.text)
print()
# Actualizar la información de un paciente
print("---------- PUT ------------")
ruta_put = url + "pacientes/1002"
update_data = {
    "nombre": "Kevin",
    "edad": 60
}
put_response = requests.put(ruta_put, json=update_data)
print(put_response.text)
# Eliminar un paciente
print("---------- DELETE ------------")
delete_paciente = url + "pacientes/1001"
response_delete = requests.delete(delete_paciente)
print(response_delete.text)