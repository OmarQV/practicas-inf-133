from http.server import HTTPServer, BaseHTTPRequestHandler
import json
# Manejo de parametros de consulta "query parameters"
from urllib.parse import urlparse, parse_qs

patients = [
   {
      "ci": 1001,
      "nombre": "Omar",
      "apellido": "Quispe",
      "edad": 21,
      "genero": "M",
      "diagnostico": "Diabetes",
      "doctor": "Lucas"
   },
   {
      "ci": 1002,
      "nombre": "Maria",
      "apellido": "Vega",
      "edad": 35,
      "genero": "F",
      "diagnostico": "Hipertensión",
      "doctor": "Juan"
   }
]

class PatientsService: 
   @staticmethod
   def find_patient(ci):
      for patient in patients:
         if patient["ci"] == ci:
            return patient
      return None
   
   @staticmethod
   def find_pacient_diagnostic(diagnostico):
      patients_filtered = []
      for patient in patients:
         if patient["diagnostico"] == diagnostico:
            patients_filtered.append(patient)
      return patients_filtered
   
   @staticmethod
   def find_pacient_doctor(doctor):
      patients_filtered = []
      for patient in patients:
         if patient["doctor"] == doctor:
            patients_filtered.append(patient)
      return patients_filtered
   
   @staticmethod
   def add_patient(data):
      data["ci"] = len(patients) + 1
      patients.append(data)
      return data
   
   @staticmethod
   def update_patient(ci, data):
      patient = PatientsService.find_patient(ci)
      if patient: 
         patient.update(data)
         return patient
      else: 
         return None
        
   @staticmethod
   def delete_patient(ci):
      patient = PatientsService.find_patient(ci)
      if patient:
         patients.remove(patient)
         return patient
      else: 
         return None
   
   

class HTTPResponseHandler:
   @staticmethod
   def handle_response(handler, status, data):
      handler.send_response(status)
      handler.send_header("Content-type", "application/json")
      handler.end_headers()
      handler.wfile.write(json.dumps(data).encode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
   def read_data(self):
      content_length = int(self.headers["Content-Length"])
      data = self.rfile.read(content_length)
      data = json.loads(data.decode("utf-8"))
      return data
     
   def do_GET(self):
      parsed_path = urlparse(self.path)
      query_params = parse_qs(parsed_path.query)
      if parsed_path.path == "/pacientes":
         HTTPResponseHandler.handle_response(self, 200, patients)
      elif parsed_path.path == "/pacientes":
         if "diagnostico" in query_params:
            diagnostico = query_params["diagnostico"][0]
            patients_filtred = PatientsService.find_pacient_diagnostic(diagnostico)
            if patients_filtred != []:
               HTTPResponseHandler.handle_response(self, 200, patients_filtred)
            else:
               HTTPResponseHandler.handle_response(self, 204, [])
         elif "doctor" in query_params:
            doctor = query_params["doctor"][0]
            patients_filtred = PatientsService.find_pacient_doctor(doctor)
            if patients_filtred:
               HTTPResponseHandler.handle_response(self, 200, patients_filtred)
            else:
               HTTPResponseHandler.handle_response(self, 204, [])
      elif self.path.startswith("/pacientes/"):
         ci = int(self.path.split("/")[-1])
         patient = PatientsService.find_patient(ci)
         if patient:
            HTTPResponseHandler.handle_response(self, 200, patient)
         else:
            HTTPResponseHandler.handle_response(self, 204, [])
      else:
         HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
         
         
   def do_POST(self):
      if self.path.startswith("/pacientes"):
         data = self.read_data()
         patient = PatientsService.add_patient(data)
         HTTPResponseHandler.handle_response(self, 200, patient)
      else:
         HTTPResponseHandler.handle_response(self, 404, {"Error":"Ruta no existente"})
   
   
   def do_PUT(self):
      if self.path.startswith("/pacientes/"):
         ci = int(self.path.split("/")[-1])
         data = self.read_data()
         patients = PatientsService.update_patient(ci, data)
         if patients:
               HTTPResponseHandler.handle_response(self, 200, patients)
         else:
               HTTPResponseHandler.handle_response(
                  self, 404, {"Error": "Estudiante no encontrado"}
               )
      else:
         HTTPResponseHandler.handle_response(
               self, 404, {"Error": "Ruta no existente"}
         )

   def do_DELETE(self):
      
      if self.path.startswith("/pacientes/"):
         ci = int(self.path.split("/")[-1])
         patient = PatientsService.delete_patient(ci)
         if patient:
               HTTPResponseHandler.handle_response(self, 200, [patient])
         else:
               HTTPResponseHandler.handle_response(self, 404, "Patient not found")
      else:
         HTTPResponseHandler.handle_response(
               self, 404, {"Error": "Ruta no existente"}
         )




def run_server(port = 8000):
   try:
      server_address = ('', port)
      httpd = HTTPServer(server_address, RESTRequestHandler)
      print(f'Iniciando servidor web en http://localhost:{port}/')
      httpd.serve_forever()
   except KeyboardInterrupt:
      print("Apagando el servidor...")
      httpd.socket.close()
      
if __name__ == "__main__":
   run_server()