import requests
import json

url = "http://localhost:8000/animales"
headers = {"Content-Type": "application/json"}

# Datos para la petición POST (Añadir un nuevo animal)
new_animal_data = {
   "animal_type": "mamifero",
   "name": "Elefante",
   "species": "africana",
   "gender": "Male",
   "age": 15,
   "weight": 5000
}

# Petición POST para añadir un nuevo animal
response = requests.post(url=url, json=new_animal_data, headers=headers)
print("Respuesta POST:", response.json())

# Datos para la petición PUT (Actualizar un animal existente)
update_animal_data = {
   "weight": 1500
}

# Petición PUT para actualizar un animal existente (se asume que el animal con ID 1 ya existe)
update_response = requests.put(f"{url}/0", json=update_animal_data, headers=headers)
print("Respuesta PUT:", update_response.json())

# Petición GET para obtener todos los animales
get_response = requests.get(url)
print("Respuesta GET:", get_response.json())

# Petición DELETE para eliminar un animal (se asume que el animal con ID 1 existe)
delete_response = requests.delete(f"{url}/0")
print("Respuesta DELETE:", delete_response.json())