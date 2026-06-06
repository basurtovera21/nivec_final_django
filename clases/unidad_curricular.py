#Enum
from clases.enums.tipo_de_componente import TipoDeComponente

#Interfaz
from clases.i_unidad_evaluable import IUnidadEvaluable


class UnidadCurricular(IUnidadEvaluable):
    def __init__(self, codigo_de_unidad: str, nombre: str, area_de_conocimiento: list, horas_totales: float, horas_semanales: float, horas_sincronicas: float, horas_asincronicas: float, tipo_de_componente: TipoDeComponente, criterio_de_aprobacion: float = 7.0, porcentaje_minimo_asistencia: float = 70.0):
        self.codigo_de_unidad = codigo_de_unidad
        self.nombre = nombre
        self.area_de_conocimiento = area_de_conocimiento #Lista
        self.horas_totales = horas_totales
        self.horas_semanales = horas_semanales
        self.horas_sincronicas = horas_sincronicas
        self.horas_asincronicas = horas_asincronicas
        self.tipo_de_componente = tipo_de_componente #Instancia
        self.criterio_de_aprobacion = criterio_de_aprobacion
        self.porcentaje_minimo_asistencia = porcentaje_minimo_asistencia
        

    def obtener_codigo_de_unidad(self):
        return self.codigo_de_unidad


    def obtener_horas_totales(self):
        return self.horas_totales


    def validar_distribucion_de_horas_totales(self):
        calculo_horas_totales = self.horas_sincronicas + self.horas_asincronicas
        if calculo_horas_totales == self.horas_totales:
            print(f"[Unidad curricular] La distribución válida.")
            return True
        
        else:
            print(f"[Unidad curricular] La distribución no es válida.")
            return False

    def visualizar_detalles_de_configuracion(self):
        print(f"Unidad curricular: {self.nombre} ({self.codigo_de_unidad})")
        print(f"Área(s) de conocimiento: {', '.join(self.area_de_conocimiento)}")
        print(f"Tipo de componente: {self.tipo_de_componente.value}")
        print(f"Horas totales: {self.horas_totales}") 
        print(f"Horas semanales: {self.horas_semanales}")
        print(f"Horas sincrónicas: {self.horas_sincronicas}") 
        print(f"Horas asincrónicas: {self.horas_asincronicas}")
        print(f"Criterio de aprobación (puntaje mínimo): {self.criterio_de_aprobacion}")
        print(f"Porcentaje mínimo de asistencia: {self.porcentaje_minimo_asistencia}%")
        print(f"Distribución de horas válida: {self.validar_distribucion_de_horas_totales()}")