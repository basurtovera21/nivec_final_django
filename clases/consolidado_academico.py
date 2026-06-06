from datetime import date

from clases.periodo_de_nivelacion import PeriodoDeNivelacion


class ConsolidadoAcademico:
    def __init__(self, periodo_academico: PeriodoDeNivelacion, fecha_de_corte: date, total_de_cupos_aceptados: int):
        self.periodo_academico = periodo_academico #Instancia o código de PeriodoDeNivelacion
        self.fecha_de_corte = fecha_de_corte #Instancia datetime.date
        self.total_de_cupos_aceptados = total_de_cupos_aceptados
        self._registros_totales = 0
        self._registros_validos = 0
        self._registros_observados = 0
        self._registros_de_entrada = [] #Lista de diccionarios o filas del archivo
        

    def verificar_aceptacion_cupo(self, identificacion: str):
        #Verificación en los registros válidos de la MTN
        for registro in self._registros_de_entrada:
            if registro.get("identificacion") == identificacion:
                return True
        return False