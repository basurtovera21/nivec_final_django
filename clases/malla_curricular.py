#Enums
from clases.enums.estado_de_malla import EstadoDeMalla
from clases.enums.modalidad import Modalidad

#Interfaz
from clases.i_unidad_evaluable import IUnidadEvaluable


class MallaCurricular:
    def __init__(self, codigo_de_malla: str, nombre: str, area_de_conocimiento: str, duracion_semanas: int, version_de_malla: str, modalidad: Modalidad):
        self.codigo_de_malla = codigo_de_malla
        self.nombre = nombre
        self.area_de_conocimiento = area_de_conocimiento
        self.duracion_semanas = duracion_semanas
        self.version_de_malla = version_de_malla
        self.modalidad = modalidad #Instancia
        self._estado = EstadoDeMalla.DISENO
        self._total_horas_nivelacion = 0.0
        self._unidades_curriculares = [] #Lista unidades curriculares
        

    def agregar_unidad_curricular(self, *args): #Sobrecarga
        for entrada in args:
            if isinstance(entrada, list):
                #Lista como argumento único
                for unidad in entrada:
                    self._agregar_una_unidad_curricular(unidad)
            else:
                self._agregar_una_unidad_curricular(entrada)
                
                
    def _agregar_una_unidad_curricular(self, unidad_curricular: IUnidadEvaluable):
        if self._estado not in (EstadoDeMalla.DISENO, EstadoDeMalla.ACTIVA):
            print(f"[Malla curricular] La malla curricular no puede ser modificada (estado actual '{self._estado.value}')")
            return

        if not isinstance(unidad_curricular, IUnidadEvaluable):
            print("[Malla curricular] La entrada no es válida.")
            return

        for unidad in self._unidades_curriculares:
            if unidad.codigo_de_unidad == unidad_curricular.codigo_de_unidad:
                print(f"[Malla curricular] La unidad ({unidad_curricular.codigo_de_unidad}) ya ha sido registrada.")
                return

        self._unidades_curriculares.append(unidad_curricular)
        self._total_horas_nivelacion = self.calcular_total_horas_nivelacion()

        print(f"[Malla curricular] La unidad ha sido registrada: {unidad_curricular.nombre}")
       
            
    def calcular_total_horas_nivelacion(self):
        calculo_total_horas_nivelacion = 0

        for unidad in self._unidades_curriculares:
            calculo_total_horas_nivelacion += unidad.obtener_horas_totales()

        return calculo_total_horas_nivelacion