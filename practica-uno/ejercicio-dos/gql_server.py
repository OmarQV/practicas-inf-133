# >> pip install graphene
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Schema, Field, Mutation

# Clase - Planta
class Planta(ObjectType):
   id = Int()
   nombre = String()
   especie = String()
   edad = Int()
   altura = Int()
   frutos = Boolean()

# -----------------------------
class Query(ObjectType):
   plantas = List(Planta)
   plantas_especie = Field(Planta, especie = String())
   plantas_frutos = List(Planta, frutos = Boolean())
   
   def resolve_plantas(root, info):
      return plantas
   
   def resolve_plantas_especie(root, info, especie):
      for planta in plantas:
         if planta.especie == especie:
            return planta
      return None
   
   def resolve_plantas_frutos(root, info, frutos):
      plantasFrutos = list(planta for planta in plantas if planta.frutos == frutos)
      return plantasFrutos
   
# clase Crear Planta
class CrearPlanta(Mutation):
   class Arguments:
      nombre = String()
      especie = String()
      edad = Int()
      altura = Int()
      frutos = Boolean()
   planta = Field(Planta)
   
   def mutate(root, info, nombre, especie, edad, altura, frutos):
      nueva_planta = Planta(
         id = len(plantas) + 1,
         nombre = nombre,
         especie = especie,
         edad = edad,
         altura = altura,
         frutos = frutos
      )
      
      plantas.append(nueva_planta)
      return CrearPlanta(planta = nueva_planta)

# Clase Actualizar
class UpdatePlanta(Mutation):
   class Arguments:
      id = Int()
      especie = String()
      edad = Int()
   
   planta = Field(Planta)
   
   def mutate(root, info, id, especie, edad):
      for planta in plantas:
         if planta.id == id:
            planta.especie = especie
            planta.edad = edad
            return UpdatePlanta(planta=planta)
      return None

# Clase Eliminar
class DeletePlanta(Mutation):
   class Arguments:
      id = Int()
      
   planta = Field(Planta)
   
   def mutate(root, info, id):
      for i, planta in enumerate(plantas):
         if planta.id == id:
            plantas.pop(i)
            return DeletePlanta(planta=planta)
      return None

#
class Mutations(ObjectType):
   crear_planta = CrearPlanta.Field()
   update_planta = UpdatePlanta.Field()
   delete_planta = DeletePlanta.Field()


plantas = [
   Planta(
      id = 1,
      nombre = "Rosa",
      especie = "Rosaceae",
      edad = 2,
      altura = 60,
      frutos = True
   ),
   Planta(
      id = 2,
      nombre = "Fresa",
      especie = "Fragaria",
      edad = 1,
      altura = 1,
      frutos = True
   )
]

schema = Schema(query=Query, mutation=Mutations)

class GraphQLRequestHandler(BaseHTTPRequestHandler):
   def response_handler(self, status, data):
      self.send_response(status)
      self.send_header("Content-type", "aplication/json")
      self.end_headers()
      self.wfile.write(json.dumps(data).encode("utf-8"))
      
   
   def do_POST(self):
      if self.path == "/graphql":
         content_length = int(self.headers["Content-Length"])
         data = self.rfile.read(content_length)
         data = json.loads(data.decode("utf-8"))
         result = schema.execute(data["query"])
         self.response_handler(200, result.data)
      else:
         self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port = 8000):
   try:
      server_address = ("", port)
      httpd = HTTPServer(server_address, GraphQLRequestHandler)
      print(f"Iniciando servidor web en https://localhost:{port}/")
      httpd.serve_forever()
   except KeyboardInterrupt:
      print("Apagando servidor web")
      httpd.socket.close()

if __name__ == "__main__":
   run_server()