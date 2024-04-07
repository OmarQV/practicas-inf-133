from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

patients = {}

class Patient:
   def __init__(self):
      self.nombre = None
      self.apellido = None
      self.edad = 0
      self.genero = None
      self.diagnostico = None
      self.doctor = None
      
   def __str__(self):
      return f"Nombre: {self.nombre}, Apellido: {self.apellido}, Edad: {self.edad}, Género: {self.genero}, Diagnóstico: {self.diagnostico}, Doctor: {self.doctor}"

class PatientBuilder:
   def __init__(self):
      self.patient = Patient()
      
   def set_nombre(self, nombre):
      self.patient.nombre = nombre
   
   def set_apellido(self, apellido):
      self.patient.apellido = apellido
      
   def set_edad(self, edad):
      self.patient.edad = edad
      
   def set_genero(self, genero):
      self.patient.genero = genero
      
   def set_diagnostico(self, diagnostico):
      self.patient.diagnostico = diagnostico
   
   def set_doctor(self, doctor):  # Agregar el método set_doctor
      self.patient.doctor = doctor
   
   def get_patient(self):
      return self.patient
   
class Hospital:
   def __init__(self, builder):
      self.builder = builder
   
   def create_patient(self, nombre, apellido, edad, genero, diagnostico, doctor):
      self.builder.set_nombre(nombre)
      self.builder.set_apellido(apellido)
      self.builder.set_edad(edad)
      self.builder.set_genero(genero)
      self.builder.set_diagnostico(diagnostico)
      self.builder.set_doctor(doctor)
      return self.builder.get_patient()


class PatientsService(BaseHTTPRequestHandler):
   def __init__(self):
      self.builder = PatientBuilder()
      self.hospital = Hospital(self.builder)
   
   def add_patient(self, data):
      nombre = data.get("nombre", None)
      apellido = data.get("apellido", None)
      edad = data.get("edad", None)
      genero = data.get("genero", None)
      diagnostico = data.get("diagnostico", None)
      doctor = data.get("doctor", None) 
      
      patient = self.hospital.create_patient(nombre, apellido, edad, genero, diagnostico, doctor)
      patients[len(patients) + 1] = patient
      return patient
   
   def list_patients(self):
      return {index: patient.__dict__ for index, patient in patients.items()}
   
   def find_patient(ci):
      for i, patient in patients.items() :
         if i == ci:
            return patient

   def find_pacient_diagnostic(self, diagnostico):
      patients_filtered = []
      for patient in patients:
         if patient["diagnostico"] == diagnostico:
            patients_filtered.append(patient)
      return patients_filtered
   
   def find_pacient_doctor(self, doctor):
      patients_filtered = []
      for patient in patients:
         if patient["doctor"] == doctor:
            patients_filtered.append(patient)
      return patients_filtered
   
   def update_patient(self, ci, data):
      if ci in patients:
         patient = patients[ci]
         nombre = data.get("nombre", None)
         apellido = data.get("apellido", None)
         edad = data.get("edad", None)
         genero = data.get("genero", None)
         diagnostico = data.get("diagnostico", None)
         doctor = data.get("doctor", None)
         
         if nombre:
               patient.nombre = nombre
         if apellido:
               patient.apellido = apellido
         if edad:
               patient.edad = edad
         if genero:
               patient.genero = genero
         if diagnostico:
               patient.diagnostico = diagnostico
         if doctor:
               patient.doctor = doctor
         
         return patient
      else:
         return None
   
   def delete_patient(self, ci):
      if ci in patients:
         del patients[ci]
         return {"message": "Vehículo eliminado"}
      else:
         return None


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

class PatientRequestHandler(BaseHTTPRequestHandler):
   def __init__(self, *args, **kwargs):
      self.controller = PatientsService()
      super().__init__(*args, **kwargs)
     
   def do_GET(self):
      parsed_path = urlparse(self.path)
      query_params = parse_qs(parsed_path.query)
      
      if parsed_path.path == "/pacientes":
         response_data = self.controller.list_patients()
         HTTPDataHandler.handle_response(self, 200, response_data)
         
      elif parsed_path.path == "/pacientes":
         if "diagnostico" in query_params:
            diagnostico = query_params["diagnostico"][0]
            patients_filtred = self.controller.find_pacient_diagnostic(diagnostico)
            if patients_filtred:
               HTTPDataHandler.handle_response(self, 200, patients_filtred)
            else:
               HTTPDataHandler.handle_response(self, 404, {"message": "Paciente no encontrado"})
         elif "doctor" in query_params:
            doctor = query_params["doctor"][0]
            patients_filtred = self.controller.find_pacient_doctor(doctor)
            if patients_filtred:
               HTTPDataHandler.handle_response(self, 200, patients_filtred)
            else:
               HTTPDataHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
      
      elif self.path.startswith("/pacientes/"):
         ci = int(self.path.split("/")[2])
         patient = self.controller.find_patient(ci)
         if patient:
            HTTPDataHandler.handle_response(self, 200, patient.__dict__)
         else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Paciente no encontrado"})
      else:
         HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no existente"})
         
         
   def do_POST(self):
      if self.path.startswith("/pacientes"):
         data = HTTPDataHandler.handle_reader(self)
         response_data = self.controller.add_patient(data)
         HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
      else:
         HTTPDataHandler.handle_response(self, 404, {"message":"Ruta no existente"})
   
   
   def do_PUT(self):
      if self.path.startswith("/pacientes/"):
         ci = int(self.path.split("/")[-1])
         data = HTTPDataHandler.handle_reader(self)
         response_data = PatientsService.update_patient(ci, data)
         if patients:
               HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
         else:
            HTTPDataHandler.handle_response(
                  self, 404, {"message": "Paciente no encontrado"}
               )
      else:
         HTTPDataHandler.handle_response(
               self, 404, {"message": "Ruta no existente"}
         )

   def do_DELETE(self):
      
      if self.path.startswith("/pacientes/"):
         ci = int(self.path.split("/")[2])
         response_data = self.controller.delete_patient(ci)
         if response_data:
               HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
         else:
               HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no existente"})
      else:
         HTTPDataHandler.handle_response(
               self, 404, {"message": "Ruta no existente"}
         )


def run_server(port = 8000):
   try:
      server_address = ('', port)
      httpd = HTTPServer(server_address, PatientRequestHandler)
      print(f'Iniciando servidor web en http://localhost:{port}/')
      httpd.serve_forever()
   except KeyboardInterrupt:
      print("Apagando el servidor...")
      httpd.socket.close()
      
if __name__ == "__main__":
   run_server()