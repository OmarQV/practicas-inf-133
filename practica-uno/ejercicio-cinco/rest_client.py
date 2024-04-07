import requests

url = "http://localhost:8000/animales"


print("\nCreando un nuevo animal:")
nuevo_animal_1 = {
   "nombre": "Leon",
   "especie": "Leon",
   "genero": "Masculino",
   "edad": 5,
   "peso": 200
}
post_response = requests.request(method="POST", url=url, json=nuevo_animal_1)
print(post_response.text)

# Listar todos los animales
print("\nListando todos los animales:")
get_response = requests.request(method="GET", url=url)
print(get_response.text)

# Buscar animales por especie
print("\nBuscando animales por especie (Tigre):")
get_response = requests.request(method="GET", url=f"{url}?especie=Tigre")
print(get_response.text)

# Buscar animales por género
print("\nBuscando animales por género (Masculino):")
get_response = requests.request(method="GET", url=f"{url}?genero=Masculino")
print(get_response.text)

# Actualizar la información de un animal
print("\nActualizando la información de un animal:")
nuevo_animal_2 = {
   "nombre": "Elefante",
   "genero": "Masculino",
   "edad": 8,
   "peso": 1000
}
put_response = requests.request(method="PUT", url=f"{url}/1", json=nuevo_animal_2)
print(put_response.text)

# Eliminar un animal
print("\nEliminando un animal:")
delete_repsonse = requests.request(method="DELETE", url=f"{url}/2")
print(delete_repsonse.text)