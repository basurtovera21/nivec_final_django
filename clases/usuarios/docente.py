#Enums
from clases.enums.tipo_de_vinculacion import TipoDeVinculacion
from clases.enums.tiempo_de_dedicacion import TiempoDeDedicacion
from clases.enums.estado_de_vinculacion import EstadoDeVinculacion

#Herencia
from clases.usuarios.usuario_academico import UsuarioAcademico


class Docente(UsuarioAcademico):
    def __init__(self, tipo_de_identificacion, identificacion: str, nombres: str, apellidos: str, correo_institucional: str, contrasena: str, fecha_de_nacimiento, sexo: str, etnia: str, porcentaje_de_discapacidad: float, celular: str, direccion: str, identificador_institucional: str, tipo_de_vinculacion: TipoDeVinculacion, tiempo_de_dedicacion: TiempoDeDedicacion, carga_horaria_maxima: float, **kwargs):
        super().__init__(
            tipo_de_identificacion = tipo_de_identificacion,
            identificacion = identificacion,
            nombres = nombres,
            apellidos = apellidos,
            correo_institucional = correo_institucional,
            contrasena = contrasena,
            fecha_de_nacimiento = fecha_de_nacimiento,
            sexo = sexo,
            etnia = etnia,
            porcentaje_de_discapacidad = porcentaje_de_discapacidad,
            celular = celular,
            direccion = direccion,
            identificador_institucional = identificador_institucional,
            **kwargs
        )
        self.tipo_de_vinculacion = tipo_de_vinculacion #Instancia
        self.tiempo_de_dedicacion = tiempo_de_dedicacion #Instancia
        self._estado_de_vinculacion = EstadoDeVinculacion.ACTIVO
        self.carga_horaria_maxima = carga_horaria_maxima #Límite normativo
        self._carga_horaria_actual = 0.0
        self._especialidades = [] #Áreas de conocimiento
        self._disponibilidad_semanal = [] #Bloque horario
        
        
    def iniciar_sesion(self): #Sobreescritura
        if self._estado_de_vinculacion.value == "Inactivo":
            print(f"[Docente] Inicio de sesión fallido: {self.nombres} {self.apellidos} (estado de vinculación inactiva).")

        else:
            print(f"[Docente] Sesión iniciada: {self.nombres} {self.apellidos} (carga horaria actual de {self._carga_horaria_actual} horas)")
         
         
    def visualizar_carga_academica(self):
        print(f"Docente: {self.nombres} {self.apellidos}")
        print(f"Carga horaria actual: {self._carga_horaria_actual} horas")
        print(f"Carga horaria máxima: {self.carga_horaria_maxima} horas")
        print(f"Horas disponibles: {self.carga_horaria_maxima - self._carga_horaria_actual} horas")
        if self._especialidades:
            print("Especialidades:", ", ".join(self._especialidades))
            
        else:
            print("Especialidades: No existe registro.")
      
            
    def inhabilitar_perfil(self):
        self._estado_de_vinculacion = EstadoDeVinculacion.INACTIVO
        print(f"El perfil ha sido inhabilitado.")