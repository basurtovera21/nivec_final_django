from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from clases.enums.dia_de_semana import DiaDeSemana
from clases.enums.estado_de_aprobacion import EstadoDeAprobacion
from clases.enums.estado_de_cohorte import EstadoDeCohorte
from clases.enums.estado_de_informe import EstadoDeInforme
from clases.enums.estado_de_malla import EstadoDeMalla
from clases.enums.estado_de_matricula import EstadoDeMatricula
from clases.enums.estado_de_periodo import EstadoDePeriodo
from clases.enums.estado_de_usuario import EstadoDeUsuario
from clases.enums.estado_de_vinculacion import EstadoDeVinculacion
from clases.enums.jornada import Jornada
from clases.enums.modalidad import Modalidad
from clases.enums.perfil_administrativo import PerfilAdministrativo
from clases.enums.registro_de_cupo import RegistroDeCupo
from clases.enums.tiempo_de_dedicacion import TiempoDeDedicacion
from clases.enums.tipo_de_cohorte import TipoDeCohorte
from clases.enums.tipo_de_componente import TipoDeComponente
from clases.enums.tipo_de_identificacion import TipoDeIdentificacion
from clases.enums.tipo_de_informe import TipoDeInforme
from clases.enums.tipo_de_sesion import TipoDeSesion
from clases.enums.tipo_de_vinculacion import TipoDeVinculacion


def cambiar_enum_a_choices(enum_clase): #Enum a choices
    choices = []

    for opcion in enum_clase:
        choices.append((opcion.value, opcion.value))

    return choices

#Entidades base
class Universidad(models.Model):
    nombre = models.CharField(max_length = 200)
    abreviatura = models.CharField(max_length = 20)
    codigo_sniese = models.CharField(max_length = 50, unique = True)
    direccion_matriz = models.CharField(max_length = 300)
    identificador_visual = models.ImageField(upload_to = "logos/", null = True, blank = True)

    class Meta:
        verbose_name        = "Universidad"
        verbose_name_plural = "Universidades"

    def __str__(self):
        return self.nombre


class Campus(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete = models.PROTECT, related_name = "campus")
    codigo_de_campus = models.CharField(max_length = 50, unique = True)
    nombre = models.CharField(max_length = 200)
    direccion_fisica = models.CharField(max_length = 300)
    provincia = models.CharField(max_length = 100)
    infraestructura_compartida = models.BooleanField(default = False)

    class Meta:
        verbose_name        = "Campus"
        verbose_name_plural = "Campus"

    def __str__(self):
        return self.nombre


class Carrera(models.Model):
    campus = models.ForeignKey(Campus, on_delete = models.PROTECT, related_name = "carreras")
    codigo_de_carrera = models.CharField(max_length = 50, unique = True)
    nombre = models.CharField(max_length = 200)
    modalidad = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(Modalidad))
    campo_de_conocimiento = models.CharField(max_length = 200)
    vigencia_sniese = models.DateField()

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"

    def __str__(self):
        return self.nombre

    def esta_activa(self):
        from clases.carrera import Carrera as CarreraBase
        from clases.enums.modalidad import Modalidad as ModalidadBase
        carrera = CarreraBase(
            codigo_de_carrera = self.codigo_de_carrera,
            nombre = self.nombre,
            modalidad = ModalidadBase(self.modalidad),
            campo_de_conocimiento = self.campo_de_conocimiento,
            vigencia_sniese = self.vigencia_sniese
        )
        return carrera.esta_activa()


#Usuarios
class CreadorDeUsuarios(BaseUserManager): #Creación de usuarios del sistema
    def create_user(self, correo_institucional, password = None, **kwargs):
        if not correo_institucional:
            raise ValueError("No se ha proporcionado un correo institucional.") #Excepción
        correo_institucional = self.normalize_email(correo_institucional) #Dar formato
        usuario_de_sistema = self.model(correo_institucional = correo_institucional, **kwargs)
        usuario_de_sistema.set_password(password) #Cifrar y guardar contraseña
        usuario_de_sistema.save(using = self._db) #Insertar registro
        return usuario_de_sistema

    def create_superuser(self, correo_institucional, password = None, **kwargs):
        kwargs.setdefault("is_staff", True) #Valores por defecto
        kwargs.setdefault("is_superuser", True) #Valores por defecto
        return self.create_user(correo_institucional, password, **kwargs)


class UsuarioDeSistema(AbstractBaseUser, PermissionsMixin):
    tipo_de_identificacion = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(TipoDeIdentificacion))
    identificacion = models.CharField(max_length = 20, unique = True)
    nombres = models.CharField(max_length = 150)
    apellidos = models.CharField(max_length = 150)
    correo_institucional = models.EmailField(unique = True)
    fecha_de_nacimiento = models.DateField(null = True, blank = True)
    sexo = models.CharField(max_length = 20)
    etnia = models.CharField(max_length = 50)
    porcentaje_de_discapacidad = models.FloatField(default = 0.0)
    celular = models.CharField(max_length = 15)
    direccion = models.CharField(max_length = 300)
    estado_de_usuario = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(EstadoDeUsuario), default = EstadoDeUsuario.PENDIENTE.value)
    is_active = models.BooleanField(default = True) #Control interno de autenticación de Django
    is_staff = models.BooleanField(default = False) #Acceso a /admin

    objects = CreadorDeUsuarios() #Administrador de la tabal

    USERNAME_FIELD  = "correo_institucional" #Identificador para iniciar sesión
    REQUIRED_FIELDS = ["identificacion", "nombres", "apellidos"] #Datos adicionales para crear superusuarios

    class Meta:
        verbose_name = "Usuario del sistema"
        verbose_name_plural = "Usuarios del sistema"

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.correo_institucional})"


class PerfilDocente(models.Model):
    usuario_de_sistema = models.OneToOneField(UsuarioDeSistema, on_delete = models.CASCADE, related_name = "perfil_docente")
    identificador_institucional = models.CharField(max_length = 50, unique = True)
    tipo_de_vinculacion = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(TipoDeVinculacion))
    tiempo_de_dedicacion = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(TiempoDeDedicacion))
    estado_de_vinculacion = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(EstadoDeVinculacion), default = EstadoDeVinculacion.ACTIVO.value)
    carga_horaria_maxima = models.FloatField(default = 40.0)
    carga_horaria_actual = models.FloatField(default = 0.0)
    especialidades = models.JSONField(default = list)  # Lista de strings

    class Meta:
        verbose_name = "Perfil docente"
        verbose_name_plural = "Perfiles docentes"

    def __str__(self):
        return f"DOCENTE: {self.usuario_de_sistema.nombres} {self.usuario_de_sistema.apellidos}"


class PerfilEstudiante(models.Model):
    usuario_de_sistema = models.OneToOneField(UsuarioDeSistema, on_delete = models.CASCADE, related_name = "perfil_estudiante")
    identificador_institucional = models.CharField(max_length = 50, unique = True)
    numero_de_matricula = models.CharField(max_length = 50, unique = True)
    jornada = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(Jornada))
    registro_de_cupo = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(RegistroDeCupo))
    carrera_registrada = models.ForeignKey(Carrera, on_delete = models.PROTECT, related_name = "estudiantes")
    campus_registrado = models.ForeignKey(Campus, on_delete = models.PROTECT, related_name = "estudiantes")
    estado_de_matricula = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(EstadoDeMatricula), default = EstadoDeMatricula.ASPIRANTE.value)
    
    class Meta:
        verbose_name = "Perfil estudiante"
        verbose_name_plural = "Perfiles estudiantes"

    def __str__(self):
        return f"ESTUDIANTE: {self.usuario_de_sistema.nombres} {self.usuario_de_sistema.apellidos}"


class PerfilAdministrativo(models.Model):
    usuario_de_sistema = models.OneToOneField(UsuarioDeSistema, on_delete = models.CASCADE, related_name = "perfil_administrativo")
    identificador_administrativo = models.CharField(max_length = 50, unique = True)
    perfil_administrativo = models.CharField(max_length = 100, choices = cambiar_enum_a_choices(PerfilAdministrativo))
    
    class Meta:
        verbose_name = "Perfil administrativo"
        verbose_name_plural = "Perfiles administrativos"

    def __str__(self):
        return f"{self.perfil_administrativo.upper()}: {self.usuario_de_sistema.nombres} {self.usuario_de_sistema.apellidos}"
    

#Estructura académica
class MallaCurricular(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete = models.PROTECT, related_name = "mallas_curriculares")
    codigo_de_malla = models.CharField(max_length = 50, unique = True)
    nombre = models.CharField(max_length = 200)
    area_de_conocimiento = models.CharField(max_length = 200)
    duracion_semanas = models.IntegerField()
    version_de_malla = models.CharField(max_length = 20)
    modalidad = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(Modalidad))
    estado = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(EstadoDeMalla), default = EstadoDeMalla.DISENO.value)
    total_horas_nivelacion = models.FloatField(default = 0.0)

    class Meta:
        verbose_name = "Malla curricular"
        verbose_name_plural = "Mallas curriculares"

    def __str__(self):
        return f"{self.nombre} — {self.version_de_malla}"


class UnidadCurricular(models.Model):
    malla_curricular = models.ForeignKey(MallaCurricular, on_delete = models.PROTECT, related_name = "unidades_curriculares")
    codigo_de_unidad = models.CharField(max_length = 50, unique = True)
    nombre = models.CharField(max_length = 200)
    area_de_conocimiento = models.JSONField(default = list)  # Lista de strings
    horas_totales = models.FloatField()
    horas_semanales = models.FloatField()
    horas_sincronicas = models.FloatField()
    horas_asincronicas = models.FloatField()
    tipo_de_componente = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(TipoDeComponente))
    criterio_de_aprobacion = models.FloatField(default = 7.0)
    porcentaje_minimo_asistencia = models.FloatField(default = 70.0)

    class Meta:
        verbose_name = "Unidad curricular"
        verbose_name_plural = "Unidades curriculares"

    def __str__(self):
        return f"{self.codigo_de_unidad} ({self.nombre})"

    def validar_distribucion_de_horas_totales(self):
        from clases.unidad_curricular import UnidadCurricular as UnidadCurricularBase
        from clases.enums.tipo_de_componente import TipoDeComponente as TipoDeComponenteBase
        unidad_curricular = UnidadCurricularBase(
            codigo_de_unidad = self.codigo_de_unidad,
            nombre = self.nombre,
            area_de_conocimiento = self.area_de_conocimiento,
            horas_totales = self.horas_totales,
            horas_semanales = self.horas_semanales,
            horas_sincronicas = self.horas_sincronicas,
            horas_asincronicas = self.horas_asincronicas,
            tipo_de_componente = TipoDeComponenteBase(self.tipo_de_componente),
            criterio_de_aprobacion = self.criterio_de_aprobacion,
            porcentaje_minimo_asistencia = self.porcentaje_minimo_asistencia
        )
        return unidad_curricular.validar_distribucion_de_horas_totales()


class PeriodoDeNivelacion(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete = models.PROTECT, related_name = "periodos")
    codigo_periodo = models.CharField(max_length = 50, unique = True)
    anio = models.IntegerField()
    periodo = models.CharField(max_length = 50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    modalidad = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(Modalidad))
    numero_periodo = models.IntegerField()
    estado = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(EstadoDePeriodo), default = EstadoDePeriodo.PLANIFICACION.value)

    class Meta:
        verbose_name = "Periodo de nivelación"
        verbose_name_plural = "Periodos de nivelación"

    def __str__(self):
        return f"{self.periodo} ({self.estado})"

    def calcular_duracion_semanas(self):
        from clases.periodo_de_nivelacion import PeriodoDeNivelacion as PeriodoDeNivelacionBase
        from clases.enums.modalidad import Modalidad as ModalidadBase
        periodo_de_nivelacion = PeriodoDeNivelacionBase(
            codigo_periodo = self.codigo_periodo,
            anio = self.anio,
            periodo = self.periodo,
            fecha_inicio = self.fecha_inicio,
            fecha_fin = self.fecha_fin,
            modalidad = ModalidadBase(self.modalidad),
            numero_periodo = self.numero_periodo
        )
        return periodo_de_nivelacion.calcular_duracion_semanas()


class Paralelo(models.Model):
    periodo_de_nivelacion = models.ForeignKey(PeriodoDeNivelacion, on_delete = models.PROTECT, related_name = "paralelos")
    unidad_curricular = models.ForeignKey(UnidadCurricular, on_delete = models.PROTECT, related_name = "paralelos")
    codigo_de_paralelo = models.CharField(max_length = 50, unique = True)
    nombre = models.CharField(max_length = 50)
    jornada = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(Jornada))
    modalidad = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(Modalidad))
    capacidad_maxima = models.IntegerField(default = 35)
    docente_responsable = models.ForeignKey(PerfilDocente, on_delete = models.SET_NULL, null = True, blank = True, related_name = "paralelos")

    class Meta:
        verbose_name = "Paralelo"
        verbose_name_plural = "Paralelos"

    def __str__(self):
        return f"{self.nombre} - {self.unidad_curricular.nombre}"

    def tiene_cupo_disponible(self):
        return self.matriculados.count() < self.capacidad_maxima


class Horario(models.Model):
    paralelo = models.ForeignKey(Paralelo, on_delete = models.CASCADE, related_name = "horarios")
    dia_semana = models.CharField(max_length = 20, choices = cambiar_enum_a_choices(DiaDeSemana))
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    espacio_de_imparticion = models.CharField(max_length = 200)
    modalidad = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(Modalidad))
    numero_semana = models.IntegerField()
    tipo_de_sesion = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(TipoDeSesion))

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"

    def __str__(self):
        return f"{self.dia_semana}: {self.hora_inicio}-{self.hora_fin} ({self.paralelo.nombre})"

    def determinar_duracion_horas(self):
        inicio = self.hora_inicio.hour + self.hora_inicio.minute/60
        fin = self.hora_fin.hour + self.hora_fin.minute/60
        return round(fin - inicio, 2)
    
    
#Procesos académicos
class CohorteDeMatricula(models.Model):
    periodo_de_nivelacion = models.ForeignKey(PeriodoDeNivelacion, on_delete = models.PROTECT, related_name = "cohortes_de_matricula")
    codigo_de_registro = models.CharField(max_length = 50, unique = True)
    fecha_de_cierre = models.DateField()
    tipo_de_cohorte = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(TipoDeCohorte))
    estado_de_cohorte = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(EstadoDeCohorte), default = EstadoDeCohorte.ABIERTA.value)
    total_primera_matricula = models.IntegerField(default = 0)
    total_segunda_matricula = models.IntegerField(default = 0)
    total_exonerados = models.IntegerField(default = 0)

    class Meta:
        verbose_name = "Cohorte de matrícula"
        verbose_name_plural = "Cohortes de matrícula"

    def __str__(self):
        return f"{self.codigo_de_registro} ({self.tipo_de_cohorte})"

    def calcular_total_matriculados(self):
        return (self.total_primera_matricula + self.total_segunda_matricula + self.total_exonerados)


class MatriculaParalelo(models.Model): #Tabla intermedia (PerfilEstudiante y Paralelo)
    #Asignación de un estudiante a un paralelo específico.
    estudiante = models.ForeignKey(PerfilEstudiante, on_delete = models.PROTECT, related_name = "estudiantes_matriculados")
    paralelo = models.ForeignKey(Paralelo, on_delete = models.PROTECT, related_name = "estudiantes_matriculados")
    cohorte_de_matricula = models.ForeignKey(CohorteDeMatricula, on_delete = models.PROTECT, related_name = "matriculas")
    fecha_registro = models.DateField(auto_now_add = True)

    class Meta:
        verbose_name = "Matrícula en paralelo"
        verbose_name_plural = "Matrículas en paralelos"
        unique_together = ("estudiante", "paralelo") #Impide repetir la combinación

    def __str__(self):
        return f"{self.estudiante} ({self.paralelo})"


class ConsolidadoAcademico(models.Model):
    periodo_academico = models.OneToOneField(PeriodoDeNivelacion, on_delete = models.PROTECT, related_name = "consolidado_academico")
    fecha_de_corte = models.DateField()
    total_cupos_aceptados = models.IntegerField(default = 0)
    registros_totales = models.IntegerField(default = 0)
    registros_validos = models.IntegerField(default = 0)
    registros_observados = models.IntegerField(default = 0)

    class Meta:
        verbose_name = "Consolidado académico"
        verbose_name_plural = "Consolidados académicos"

    def __str__(self):
        return f"CONSOLIDADO ACADÉMICO ({self.periodo_academico.periodo})"


class EvaluacionAcademica(models.Model):
    estudiante = models.ForeignKey(PerfilEstudiante, on_delete = models.PROTECT, related_name = "evaluaciones_academicas")
    unidad_curricular = models.ForeignKey(UnidadCurricular, on_delete = models.PROTECT, related_name = "evaluaciones_academicas")
    calificacion_parcial_1 = models.FloatField(default = 0.0)
    calificacion_parcial_2 = models.FloatField(default = 0.0)
    nota_final = models.FloatField(default = 0.0)
    porcentaje_asistencia = models.FloatField(default = 0.0)
    estado_de_aprobacion = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(EstadoDeAprobacion), default = EstadoDeAprobacion.PENDIENTE.value)
    observacion = models.TextField(blank = True, default = "")

    class Meta:
        verbose_name = "Evaluación académica"
        verbose_name_plural = "Evaluaciones académicas"
        unique_together = ("estudiante", "unidad_curricular") #Impide repetir la combinación

    def __str__(self):
        return f"{self.estudiante} ({self.unidad_curricular.nombre})"
    

#Informes
class InformeGeneral(models.Model):
    periodo_academico = models.ForeignKey(PeriodoDeNivelacion, on_delete = models.PROTECT, related_name = "informes")
    codigo_de_informe = models.CharField(max_length = 100, unique = True)
    tipo_de_informe = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(TipoDeInforme))
    estado_de_informe = models.CharField(max_length = 50, choices = cambiar_enum_a_choices(EstadoDeInforme), default = EstadoDeInforme.BORRADOR.value)
    fecha_de_emision = models.DateField(null = True, blank = True)
    cohortes = models.ManyToManyField(CohorteDeMatricula, blank = True, related_name = "informes")

    class Meta:
        verbose_name = "Informe general"
        verbose_name_plural = "Informes generales"

    def __str__(self):
        return f"{self.codigo_de_informe} ({self.estado_de_informe})"