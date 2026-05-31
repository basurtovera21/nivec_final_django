from django.urls import path
from core import views


urlpatterns = [
    path("", views.iniciar_sesion, name = "iniciar_sesion"),
    path("cerrar-sesion/", views.cerrar_sesion, name = "cerrar_sesion"),
    path("panel/", views.panel_principal, name = "panel_principal"),

    #Vistas por rol
    path("panel/dan/", views.panel_dan, name = "panel_dan"),
    path("panel/coordinador-ua/", views.panel_coordinador_ua, name = "panel_coordinador_ua"),
    path("panel/docente/", views.panel_docente, name = "panel_docente"),
    path("panel/estudiante/", views.panel_estudiante, name = "panel_estudiante"),
    path("panel/administrativo/", views.panel_administrativo, name = "panel_administrativo"),

    #Entidades
    path("universidades/", views.listar_universidades, name = "listar_universidades"),
    path("universidades/registrar/", views.registrar_universidad, name = "registrar_universidad"),
    path("campus/", views.listar_campus, name = "listar_campus"),
    path("campus/registrar/", views.registrar_campus, name = "registrar_campus"),
    path("carreras/", views.listar_carreras, name = "listar_carreras"),
    path("carreras/registrar/", views.registrar_carrera, name = "registrar_carrera"),

    #Usuarios
    path("docentes/", views.listar_docentes, name = "listar_docentes"),
    path("docentes/registrar/", views.registrar_docente, name = "registrar_docente"),
    path("estudiantes/", views.listar_estudiantes, name = "listar_estudiantes"),
    path("estudiantes/registrar/", views.registrar_estudiante, name = "registrar_estudiante"),

    #Estructura académica
    path("periodos/", views.listar_periodos, name = "listar_periodos"),
    path("periodos/registrar/", views.registrar_periodo_de_nivelacion, name = "registrar_periodo_de_nivelacion"),
    path("mallas/", views.listar_mallas_curriculares, name = "listar_mallas"),
    path("mallas/registrar/", views.registrar_malla_curricular, name = "registrar_malla_curricular"),
    path("unidades/", views.listar_unidades_curriculares, name = "listar_unidades"),
    path("unidades/registrar/", views.registrar_unidades_curriculares, name = "registrar_unidades_curriculares"),
    path("paralelos/", views.listar_paralelos, name = "listar_paralelos"),
    path("paralelos/registrar/", views.registrar_paralelo, name = "registrar_paralelo"),
    path("horarios/registrar/", views.crear_horario, name = "crear_horario"),

    #MTN y consolidado
    path("mtn/procesar/", views.procesar_mtn, name = "procesar_mtn"),

    #Evaluaciones
    path("evaluaciones/", views.listar_evaluaciones, name = "listar_evaluaciones"),
    path("evaluaciones/registrar/", views.registrar_evaluacion, name = "registrar_evaluacion"),

    #Informe general
    path("informe/<int:periodo_id>/", views.crear_informe_general, name = "crear_informe_general"),
]