from http.server import HTTPServer, BaseHTTPRequestHandler
import json

animales = {}

class Animal:
   def __init__(self, animal_id, name, species, gender, age, weight):
      self.animal_id = animal_id
      self.name = name
      self.species = species
      self.gender = gender
      self.age = age
      self.weight = weight

   def __str__(self):
      return f"ID: {self.animal_id}, Name: {self.name}, Species: {self.species}, Gender: {self.gender}, Age: {self.age}, Weight: {self.weight}"

class Mamifero(Animal):
   def __init__(self, animal_id, name, species, gender, age, weight):
      super().__init__(animal_id, name, species, gender, age, weight)


class Ave(Animal):
   def __init__(self, animal_id, name, species, gender, age, weight):
      super().__init__(animal_id, name, species, gender, age, weight)


class Reptil(Animal):
   def __init__(self, animal_id, name, species, gender, age, weight):
      super().__init__(animal_id, name, species, gender, age, weight)


class Anfibio(Animal):
   def __init__(self, animal_id, name, species, gender, age, weight):
      super().__init__(animal_id, name, species, gender, age, weight)


class Pez(Animal):
   def __init__(self, animal_id, name, species, gender, age, weight):
      super().__init__(animal_id, name, species, gender, age, weight)


class AnimalFactory:
   @staticmethod
   def create_animal(animal_type, animal_id, name, species, gender, age, weight):
      if animal_type == "mamifero":
         return Mamifero(animal_id, name, species, gender, age, weight)
      elif animal_type == "ave":
         return Ave(animal_id, name, species, gender, age, weight)
      elif animal_type == "reptil":
         return Reptil(animal_id, name, species, gender, age, weight)
      elif animal_type == "anfibio":
         return Anfibio(animal_id, name, species, gender, age, weight)
      elif animal_type == "pez":
         return Pez(animal_id, name, species, gender, age, weight)
      else:
         raise ValueError("Tipo de animal no válido")

class HTTPDataHandler:
   @staticmethod
   def handle_response(handler, status, data):
      handler.send_response(status)
      handler.send_header("Content-type", "application/json")
      handler.end_headers()
      handler.wfile.write(json.dumps(data).encode("utf-8"))

   @staticmethod
   def handle_reader(handler):
      content_length = int(handler.headers["Content-Length"])
      post_data = handler.rfile.read(content_length)
      return json.loads(post_data.decode("utf-8"))

class AnimalService:
   def __init__(self):
      self.factory = AnimalFactory()
      
   def add_animal(self, data):
      if not animales:
         animal_id = 1
      else:
         animal_id = max(animales.keys()) + 1
      
      animal = self.factory.create_animal(data["animal_type"], animal_id, data["name"], data["species"], data["gender"], data["age"], data["weight"])
      animales[len(animales)] = animal
      
      return animal
   
   def __init__(self):
      self.factory = AnimalFactory()
      
   def update_animal(self, animal_id, data):
      if animal_id in animales:
         animal = animales[animal_id]
         name = data.get("name", None)
         species = data.get("species", None)
         gender = data.get("gender", None)
         age = data.get("age", None)
         weight = data.get("weight", None)
         if name:
               animal.name = name
         if species:
               animal.species = species
         if gender:
               animal.gender = gender
         if age:
               animal.age = age
         if weight:
               animal.weight = weight
         return animal
      else:
         return None
   
   def list_animal(self):
      return {index: animal.__dict__ for index, animal in animales.items()}
      
   def delete_animal(self,animal_id):
      if animal_id in animales:
         an = animales.pop(animal_id)
         return an
      else:
         return None
      
      
class ZooRequestHandler(BaseHTTPRequestHandler):
   def __init__(self, *args, **kwargs):
      self.animal_service = AnimalService()
      super().__init__(*args, **kwargs)

   def do_GET(self):
      if self.path == "/animales":
         response_data = self.animal_service.list_animal()
         if response_data:
               HTTPDataHandler.handle_response(self, 200, response_data)
         else:
               HTTPDataHandler.handle_response(self, 404, {"Message": "La lista está vacía"})

   def do_POST(self):
      if self.path == "/animales":
         data = HTTPDataHandler.handle_reader(self)
         response_data = self.animal_service.add_animal(data)
         HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
      else:
         HTTPDataHandler.handle_response(
               self, 404, {"message": "Ruta no encontrada"}
         )
   def do_PUT(self):
      if self.path.startswith("/animales/"):
         animal_id = int(self.path.split("/")[-1])
         data = HTTPDataHandler.handle_reader(self)
         response_data = self.animal_service.update_animal(animal_id, data)
         if response_data:
               HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
         else:
               HTTPDataHandler.handle_response(
                  self, 404, {"message": "Animal no encontrado"}
               )
      else:
         HTTPDataHandler.handle_response(
               self, 404, {"message": "Ruta no encontrada"}
         )
         
   def do_DELETE(self):
      if self.path.startswith("/animales/"):
         animal_id = int(self.path.split("/")[-1])
         response_data = self.animal_service.delete_animal(animal_id)
         if response_data:
               HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
         else:
               HTTPDataHandler.handle_response(
                  self, 404, {"message": "Animal no encoontrado"}
               )
      else:
         HTTPDataHandler.handle_response(
               self, 404, {"message": "Ruta no encontrada"}
         )
def main():
   try:
      server_address = ("", 8000)
      httpd = HTTPServer(server_address, ZooRequestHandler)
      print("Iniciando servidor HTTP en puerto 8000...")
      httpd.serve_forever()
   except KeyboardInterrupt:
      print("Apagando servidor HTTP")
      httpd.socket.close()


if __name__ == "__main__":
   main()