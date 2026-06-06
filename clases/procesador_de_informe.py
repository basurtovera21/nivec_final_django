#Enums
from clases.enums.formato_de_exportacion import FormatoDeExportacion

#Clases
from clases.informe_general import InformeGeneral


class ProcesadorDeInforme:
    def exportar_consolidado(self, informe_general: InformeGeneral, formato_de_exportacion: FormatoDeExportacion):
        nombre_de_archivo = f"{informe_general.codigo_de_informe}_{informe_general.tipo_de_informe.value}"

        if formato_de_exportacion == FormatoDeExportacion.PDF:
            nombre_de_archivo += ".pdf"
            self._generar_archivo_pdf(nombre_de_archivo, informe_general)

        elif formato_de_exportacion == FormatoDeExportacion.EXCEL:
            nombre_de_archivo += ".xlsx"
            self._generar_archivo_excel(nombre_de_archivo, informe_general)

        else:
            print(f"[Procesador de informe] Formato de exportación no soportado: {formato_de_exportacion}")


    def _generar_archivo_pdf(self, nombre_de_archivo: str, informe_general: InformeGeneral):
        print(f"[Procesador de informe] Archivo PDF: {nombre_de_archivo}")


    def _generar_archivo_excel(self, nombre_de_archivo: str, informe_general: InformeGeneral):
        print(f"[Procesador de informe] Archivo Excel: {nombre_de_archivo}")