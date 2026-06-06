from datetime import date

#Enum
from enums.estado_de_alerta import EstadoDeAlerta

from clases.periodo_de_nivelacion import PeriodoDeNivelacion


class MonitorNormativo:
    @staticmethod
    def evaluar_proximidad_vencimiento(periodo_de_nivelacion: PeriodoDeNivelacion, fecha_limite: date):
        #Diferencia de días respecto a la fecha actual
        dias_restantes = (fecha_limite - date.today()).days
        if dias_restantes < 0:
            estado_alerta = EstadoDeAlerta.CRITICO
        else:
            if dias_restantes <= 5:
                estado_alerta = EstadoDeAlerta.PREVENTIVO
            else:
                estado_alerta = EstadoDeAlerta.NORMAL

        return {
            "Periodo de nivelación": periodo_de_nivelacion.periodo,
            "Días restantes": dias_restantes,
            "Estado de alerta": estado_alerta.value
        }