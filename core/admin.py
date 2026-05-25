#Panel administrativo
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import (Universidad, Campus, Carrera, UsuarioDeSistema, PerfilDocente, PerfilEstudiante, PerfilAdministrativo, MallaCurricular, UnidadCurricular, PeriodoDeNivelacion, Paralelo, Horario, CohorteDeMatricula, MatriculaParalelo, ConsolidadoAcademico, EvaluacionAcademica, InformeGeneral)



@admin.register(Universidad)
class UniversidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "abreviatura", "codigo_sniese") #Columnas en tabla
    search_fields = ("nombre", "abreviatura", "codigo_sniese") #Campos de búsqueda


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ("nombre", "universidad", "provincia", "infraestructura_compartida")
    search_fields = ("nombre", "provincia")
    list_filter = ("infraestructura_compartida", "universidad") #Filtro de registros


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ("nombre", "campus", "modalidad", "vigencia_sniese")
    search_fields = ("nombre", "codigo_de_carrera")
    list_filter = ("modalidad", "campus")


@admin.register(UsuarioDeSistema)
class UsuarioDeSistemaAdmin(UserAdmin): #Panel administrativo para usuarios del sistema.
#Extiende UserAdmin para reutilizar funcionalidades de autenticación y seguridad.
    model = UsuarioDeSistema #Modelo de control
    list_display = ("identificacion", "nombres", "apellidos", "correo_institucional", "estado_de_usuario", "is_staff")
    search_fields = ("identificacion", "nombres", "apellidos", "correo_institucional")
    list_filter = ("estado_de_usuario", "is_staff", "is_active")
    ordering = ("apellidos", "nombres") #Orden de listas

    #Secciones
    fieldsets = (
        ("Identificación", {
            "fields": ("tipo_de_identificacion", "identificacion",
                       "nombres", "apellidos", "correo_institucional") #Campos
        }),
        ("Datos personales", {
            "fields": ("fecha_de_nacimiento", "sexo", "etnia",
                       "porcentaje_de_discapacidad", "celular", "direccion")
        }),
        ("Acceso", {
            "fields": ("estado_de_usuario", "is_active", "is_staff",
                       "is_superuser", "password")
        }),
    )
    #Campos de creación 
    add_fieldsets = (
        ("Nuevo usuario", {
            "classes": ("wide",), #Apariencia visual
            "fields": ("correo_institucional", "identificacion",
                       "nombres", "apellidos", "password1", "password2") #Contraseña y confirmar contraseña
        }),
    )


@admin.register(PerfilDocente)
class PerfilDocenteAdmin(admin.ModelAdmin):
    list_display = ("usuario_de_sistema", "identificador_institucional", "tipo_de_vinculacion", "tiempo_de_dedicacion", "estado_de_vinculacion", "carga_horaria_actual", "carga_horaria_maxima")
    search_fields = ("usuario_de_sistema__nombres", "usuario_de_sistema__apellidos", "identificador_institucional") # __Permite consultar atributos de modelos relacionados.
    list_filter = ("tipo_de_vinculacion", "tiempo_de_dedicacion", "estado_de_vinculacion")


@admin.register(PerfilEstudiante)
class PerfilEstudianteAdmin(admin.ModelAdmin):
    list_display = ("usuario_de_sistema", "numero_de_matricula", "carrera_registrada", "campus_registrado", "jornada", "estado_de_matricula")
    search_fields = ("usuario_de_sistema__nombres", "usuario_de_sistema__apellidos", "numero_de_matricula", "identificador_institucional")
    list_filter   = ("jornada", "estado_de_matricula", "carrera_registrada")


@admin.register(PerfilAdministrativo)
class PerfilAdministrativoAdmin(admin.ModelAdmin):
    list_display = ("usuario_de_sistema", "perfil_administrativo", "identificador_administrativo")
    search_fields = ("usuario_de_sistema__nombres", "usuario_de_sistema__apellidos", "identificador_administrativo")
    list_filter = ("perfil_administrativo",)


@admin.register(MallaCurricular)
class MallaCurricularAdmin(admin.ModelAdmin):
    list_display = ("nombre", "carrera", "version_de_malla", "modalidad", "estado", "total_horas_nivelacion")
    search_fields = ("nombre", "codigo_de_malla")
    list_filter = ("modalidad", "estado", "carrera")


@admin.register(UnidadCurricular)
class UnidadCurricularAdmin(admin.ModelAdmin):
    list_display = ("codigo_de_unidad", "nombre", "malla_curricular", "tipo_de_componente", "horas_totales", "criterio_de_aprobacion", "porcentaje_minimo_asistencia")
    search_fields = ("codigo_de_unidad", "nombre")
    list_filter = ("tipo_de_componente", "malla_curricular")


@admin.register(PeriodoDeNivelacion)
class PeriodoDeNivelacionAdmin(admin.ModelAdmin):
    list_display = ("periodo", "universidad", "anio", "numero_periodo", "modalidad", "fecha_inicio", "fecha_fin", "estado")
    search_fields = ("codigo_periodo", "periodo")
    list_filter = ("estado", "modalidad", "anio", "universidad")


@admin.register(Paralelo)
class ParaleloAdmin(admin.ModelAdmin):
    list_display = ("nombre", "periodo_de_nivelacion", "unidad_curricular", "docente_responsable", "jornada", "modalidad", "capacidad_maxima")
    search_fields = ("codigo_de_paralelo", "nombre")
    list_filter = ("jornada", "modalidad", "periodo_de_nivelacion")


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("paralelo", "dia_semana", "hora_inicio", "hora_fin", "tipo_de_sesion", "espacio_de_imparticion", "numero_semana")
    search_fields = ("paralelo__nombre", "espacio_de_imparticion")
    list_filter = ("dia_semana", "tipo_de_sesion", "modalidad")


@admin.register(CohorteDeMatricula)
class CohorteDeMatriculaAdmin(admin.ModelAdmin):
    list_display = ("codigo_de_registro", "periodo_de_nivelacion", "tipo_de_cohorte", "estado_de_cohorte", "total_primera_matricula", "total_segunda_matricula", "total_exonerados", "fecha_de_cierre")
    search_fields = ("codigo_de_registro",) #Tupla
    list_filter   = ("tipo_de_cohorte", "estado_de_cohorte", "periodo_de_nivelacion")


@admin.register(MatriculaParalelo)
class MatriculaParaleloAdmin(admin.ModelAdmin):
    list_display = ("estudiante", "paralelo", "cohorte_de_matricula", "fecha_registro")
    search_fields = ("estudiante__usuario_de_sistema__nombres", "estudiante__usuario_de_sistema__apellidos", "paralelo__nombre")
    list_filter = ("cohorte_de_matricula", "paralelo__periodo_de_nivelacion")


@admin.register(ConsolidadoAcademico)
class ConsolidadoAcademicoAdmin(admin.ModelAdmin):
    list_display = ("periodo_academico", "fecha_de_corte", "total_cupos_aceptados", "registros_totales", "registros_validos", "registros_observados")
    search_fields = ("periodo_academico__periodo",)


@admin.register(EvaluacionAcademica)
class EvaluacionAcademicaAdmin(admin.ModelAdmin):
    list_display = ("estudiante", "unidad_curricular", "calificacion_parcial_1", "calificacion_parcial_2", "nota_final", "porcentaje_asistencia", "estado_de_aprobacion")
    search_fields = ("estudiante__usuario_de_sistema__nombres", "estudiante__usuario_de_sistema__apellidos", "unidad_curricular__nombre")
    list_filter = ("estado_de_aprobacion", "unidad_curricular")


@admin.register(InformeGeneral)
class InformeGeneralAdmin(admin.ModelAdmin):
    list_display = ("codigo_de_informe", "periodo_academico", "tipo_de_informe", "estado_de_informe", "fecha_de_emision")
    search_fields = ("codigo_de_informe",)
    list_filter = ("tipo_de_informe", "estado_de_informe", "periodo_academico")