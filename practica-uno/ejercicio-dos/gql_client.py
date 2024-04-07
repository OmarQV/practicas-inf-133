import requests

url = 'http://localhost:8000/graphql'

# Crear una planta
print("\nCrear una planta")
query_crear = """
mutation {
   crearPlanta(nombre:"Cactus", especie:"Cactaceae", edad: 10, altura: 20, frutos: false) {
      planta {
         id
         nombre
         especie
         edad
         altura
         frutos
      }
   }
}
"""
response1 = requests.post(url, json={'query': query_crear})
print(response1.text)
print("-"*50)

# Listar todas las plantas
print("\nListar todas las plantas")
query_listar = """
{
   plantas {
      id
      nombre
      especie
      edad
      altura
      frutos
   }
}
"""
response2 = requests.post(url, json={'query': query_listar})
print(response2.text)
print("-"*50)

# Buscar plantas por especie
print("\nBuscar plantas por especie")
query_especie = """
{
   plantasEspecie(especie:"Rosaceae") {
      id
      nombre
   }   
}
"""
response3 = requests.post(url, json={'query': query_especie})
print(response3.text)
print("-"*50)
# Buscar las plantas que tienen frutos
print("\nBuscar plantas por frutos")
query_frutos = """
{
   plantasFrutos(frutos: false) {
      id
      nombre
   }   
}
"""
response3 = requests.post(url, json={'query': query_frutos})
print(response3.text)
print("-"*50)
# Actualizar la información de una planta
print("\nActualizar la información de una planta")
query_update = """
mutation {
   updatePlanta(id: 1, especie:"otro", edad: 55) {
      planta {
         id
         nombre
         especie
         edad
         altura
         frutos
      }
   }
}
"""
response4 = requests.post(url, json={'query': query_update})
print(response4.text)
print("-"*50)
# Eliminar una planta
print("\nEliminar una planta")
query_eliminar = """
mutation {
   deletePlanta(id: 1) {
      planta {
         id
         nombre
         especie
         edad
         altura
         frutos
      }
   }
}
"""
response5 = requests.post(url, json={'query': query_eliminar})
print(response5.text)

print()
response2 = requests.post(url, json={'query': query_listar})
print(response2.text)
print("-"*50)