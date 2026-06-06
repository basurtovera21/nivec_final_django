#Enums
from clases.enums.jornada import Jornada
from clases.enums.modalidad import Modalidad

#Usuarios
from clases.usuarios.docente import Docente
from clases.usuarios.estudiante import Estudiante


class Paralelo:
    def __init__(self, codigo_de_paralelo: str, nombre: str, jornada: Jornada, modalidad: Modalidad, capacidad_maxima: int):
        self.codigo_de_paralelo = codigo_de_paralelo
        self.nombre = nombre
        self.jornada = jornada #Instancia
        self.modalidad = modalidad #Instancia
        self.capacidad_maxima = capacidad_maxima
        self._docente_responsable = None #Instancia Docente
        self._estudiantes_matriculados = [] #Lista de instancias Estudiante
        

    def tiene_cupo_disponible(self): #Retorna bool
        total_matriculados = len(self._estudiantes_matriculados)
        
        if total_matriculados < self.capacidad_maxima:
            return True
        else:
            return False
        
            
    def vincular_estudiante(self, estudiante: Estudiante):
        if not self.tiene_cupo_disponible():
            print(f"[Paralelo] No existen cupos disponibles: {self.nombre}")
            return

        if estudiante in self._estudiantes_matriculados:
            print(f"[Paralelo] El estudiante ya ha sido registrado previamente: {estudiante.nombres} {estudiante.apellidos}")
            return

        self._estudiantes_matriculados.append(estudiante)
        print(f"[Paralelo] El estudiante ha sido registrado: {estudiante.nombres} {estudiante.apellidos}")
        
        
    def desvincular_estudiante(self, estudiante: Estudiante):
        if estudiante not in self._estudiantes_matriculados:
            print(f"[Paralelo] El estudiante no ha sido encontrado: {estudiante.nombres} {estudiante.apellidos}")
            return

        self._estudiantes_matriculados.remove(estudiante)
        print(f"[Paralelo] El estudiante ha sido removido: {estudiante.nombres} {estudiante.apellidos}")
        
        
    def vincular_docente(self, docente: Docente):
        if self._docente_responsable is not None:
            print(f"[Paralelo] El paralelo ya tiene un docente vinculado: {self._docente_responsable.nombres} {self._docente_responsable.apellidos}")
            return

        self._docente_responsable = docente
        print(f"[Paralelo] El docente ha sido vinculado: {docente.nombres} {docente.apellidos}")