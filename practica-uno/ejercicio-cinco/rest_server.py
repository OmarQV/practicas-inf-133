from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import parse_qs, urlparse
animales= []


class RESTRequestHandler(BaseHTTPRequestHandler):
   def response_handler(self, status, data):
      self.send_response(status)
      self.send_header("Content-type","application/json")
      self.end_headers()
      self.wfile.write(json.dumps(data).encode('utf-8'))
      
   def read_data(self):
      content_length = int(self.headers["Content-Length"])
      data = self.rfile.read(content_length)
      data = json.loads(data.decode('utf-8'))
      return data
   
   def find_animal_by_id(self,id):
      return next((animal for animal in animales if animal["id"] == id), None,)
   
   def do_POST(self):
      if self.path == "/animales":
         data = self.read_data()
         data["id"] = len(animales)+1
         animales.append(data)
         self.response_handler(201, animales)
   
   def do_DELETE(self):
      if self.path.startswith("/animales/"):
         index = int(self.path.split("/")[-1])
         delete_animal=None
         for i, animal in enumerate(animales):
            if animal["id"] ==index:
               delete_animal = animales.pop(i)
                  
         if delete_animal: 
            self.response_handler(200, delete_animal)
         else: 
            self.response_handler(404, {"Message":"No se encontro ningun animal con ese id"})
      else: 
         self.response_handler(404, {"Error":"ruta no existente"})
   
   def do_GET(self):
      parsed_path = urlparse(self.path)
      query_params = parse_qs(parsed_path.query)

      if parsed_path.path == "/animales":
         if "especie" in query_params:
            especie = query_params["especie"][0]
            animales_filtrados = [
               animal for animal in animales if animal["especie"] == especie
            ]
            if animales_filtrados:
               self.response_handler(200, animales_filtrados)
            else: self.response_handler(404, {"Message":"No hay animales de esa especie"})
         elif "genero" in query_params:
            genero = query_params["genero"][0]
            animales_filtrados = [
               animal for animal in animales if animal["genero"] == genero
            ]
            if animales_filtrados:
               self.response_handler(200, animales_filtrados)
            else: 
               self.response_handler(404, {"Message":"No hay animales de ese genero"})
               
         else: self.response_handler(200,animales)

      elif self.path.startswith("/animales/"):
         id = int(self.path.split("/")[-1])
         animal = self.find_animal_by_id(id)
         if animal:
            self.response_handler(200, animal)
         else: 
            self.response_handler(404, {"Mssage":"No hay animales con es ID"})
      else:
         self.response_handler(404, {"Error":"ruta no existente"})
         
   def do_PUT(self):
      if self.path.startswith("/animales/"):
         id = int(self.path.split("/")[-1])
         animal = self.find_animal_by_id(id)
         data = self.read_data()
         if animal:
            animal.update(data)
            self.response_handler(200, animal)
         else:
               self.response_handler(404, {"Error": "Animal no encontrado"})
      else:
         self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
   try:
      server_address = ("", port)
      httpd = HTTPServer(server_address, RESTRequestHandler)
      print(f"Iniciando servidor web en http://localhost:{port}/")
      httpd.serve_forever()
   except KeyboardInterrupt:
      print("Apagando servidor web")
      httpd.socket.close()


if __name__ == "__main__":
   run_server()