from django import forms
from core.models import (Universidad, Campus, Carrera, UsuarioDeSistema, PerfilDocente, PerfilEstudiante, PerfilAdministrativo, MallaCurricular, UnidadCurricular, PeriodoDeNivelacion, Paralelo, Horario, CohorteDeMatricula, EvaluacionAcademica)


#Carga de MTN 
class DocumentoMTN(forms.Form):
    documento_mtn = forms.FileField(
        label = "Documento MTN (.xlsx)",
        help_text = "Registro de Matriz de Tercer Nivel.",
    )

    def clean_documento_mtn(self): #clean; palabra reservada
        documento_mtn = self.cleaned_data.get("documento_mtn")
        if documento_mtn:
            if not documento_mtn.name.endswith(".xlsx"):
                raise forms.ValidationError("Registro no válido.")
            if documento_mtn.size > 10 * 1024 * 1024: #10MB
                raise forms.ValidationError("El documento supera el límite permitido (10MB).")
        return documento_mtn


#Universidad
class FormularioUniversidad(forms.ModelForm):
    class Meta:
        model = Universidad
        fields = ("nombre", "abreviatura", "codigo_sniese", "direccion_matriz", "identificador_visual")
        labels = {
            "nombre": "Nombre de la institución",
            "abreviatura": "Abreviatura",
            "codigo_sniese": "Código SNIESE",
            "direccion_matriz": "Dirección de matriz",
            "identificador_visual": "Identificador visual",
        }


#Campus
class FormularioCampus(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ("universidad", "codigo_de_campus", "nombre", "direccion_fisica", "provincia", "infraestructura_compartida")
        labels = {
            "universidad": "Universidad",
            "codigo_de_campus": "Código de campus",
            "nombre": "Nombre del campus",
            "direccion_fisica": "Dirección física",
            "provincia": "Provincia",
            "infraestructura_compartida": "¿Infraestructura compartida?",
        }


#Carrera
class FormularioCarrera(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ("campus", "codigo_de_carrera", "nombre", "modalidad", "campo_de_conocimiento", "vigencia_sniese")
        labels = {
            "campus": "Campus",
            "codigo_de_carrera": "Código de carrera",
            "nombre": "Nombre de la carrera",
            "modalidad": "Modalidad",
            "campo_de_conocimiento": "Campo de conocimiento",
            "vigencia_sniese": "Vigencia SNIESE",
        }
        widgets = {"vigencia_sniese": forms.DateInput(attrs = {"type": "date"})} #Fecha


#Usuario de sistema
class FormularioUsuarioDeSistema(forms.ModelForm):
    contrasena = forms.CharField(
        label = "Contraseña",
        widget = forms.PasswordInput,
        min_length = 8, max_length = 16
    )
    confirmar_contrasena = forms.CharField(
        label = "Confirmar contraseña",
        widget = forms.PasswordInput
    )

    class Meta:
        model = UsuarioDeSistema
        fields = ("tipo_de_identificacion", "identificacion", "nombres", "apellidos", "correo_institucional", "fecha_de_nacimiento", "sexo", "etnia", "porcentaje_de_discapacidad", "celular", "direccion")
        labels = {
            "tipo_de_identificacion": "Tipo de identificación",
            "identificacion": "Número de identificación",
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "correo_institucional": "Correo institucional",
            "fecha_de_nacimiento": "Fecha de nacimiento",
            "sexo": "Sexo",
            "etnia": "Etnia",
            "porcentaje_de_discapacidad": "Porcentaje de discapacidad (%)",
            "celular": "Número de celular",
            "direccion": "Dirección",
        }
        widgets = {
            "fecha_de_nacimiento": forms.DateInput(attrs = {"type": "date"})
        }

    def clean(self): #Validar contraseñas
        registro_validado = super().clean()
        if registro_validado.get("contrasena") != registro_validado.get("confirmar_contrasena"):
            raise forms.ValidationError("Los registros no son iguales.")
        return registro_validado


#Docente
class FormularioPerfilDocente(forms.ModelForm):
    class Meta:
        model = PerfilDocente
        fields = ("identificador_institucional", "tipo_de_vinculacion", "tiempo_de_dedicacion", "carga_horaria_maxima", "especialidades")
        labels = {
            "identificador_institucional": "Identificador institucional",
            "tipo_de_vinculacion": "Tipo de vinculación",
            "tiempo_de_dedicacion": "Tiempo de dedicación",
            "carga_horaria_maxima": "Carga horaria máxima (horas)",
            "especialidades": "Especialidades",
        }


#Estudiante
class FormularioPerfilEstudiante(forms.ModelForm):
    class Meta:
        model = PerfilEstudiante
        fields = ("identificador_institucional", "numero_de_matricula", "jornada", "registro_de_cupo", "carrera_registrada", "campus_registrado")
        labels = {
            "identificador_institucional": "Identificador institucional",
            "numero_de_matricula": "Número de matrícula",
            "jornada": "Jornada",
            "registro_de_cupo": "Registro de cupo",
            "carrera_registrada": "Carrera",
            "campus_registrado": "Campus",
        }


#Perfil administrativo
class FormularioPerfilAdministrativo(forms.ModelForm):
    class Meta:
        model = PerfilAdministrativo
        fields = ("identificador_administrativo", "perfil_administrativo")
        labels = {
            "identificador_administrativo": "Identificador administrativo",
            "perfil_administrativo": "Perfil administrativo",
        }


#Malla curricular
class FormularioMallaCurricular(forms.ModelForm):
    class Meta:
        model  = MallaCurricular
        fields = ("carrera", "codigo_de_malla", "nombre", "area_de_conocimiento", "duracion_semanas", "version_de_malla", "modalidad")
        labels = {
            "carrera": "Carrera",
            "codigo_de_malla": "Código de malla",
            "nombre": "Nombre de malla",
            "area_de_conocimiento": "Área de conocimiento",
            "duracion_semanas": "Duración (semanas)",
            "version_de_malla": "Versión de malla",
            "modalidad": "Modalidad",
        }


#Unidad curricular
class FormularioUnidadCurricular(forms.ModelForm):
    class Meta:
        model  = UnidadCurricular
        fields = ("malla_curricular", "codigo_de_unidad", "nombre", "area_de_conocimiento", "horas_totales", "horas_semanales", "horas_sincronicas", "horas_asincronicas", "tipo_de_componente", "criterio_de_aprobacion", "porcentaje_minimo_asistencia")
        labels = {
            "malla_curricular": "Malla curricular",
            "codigo_de_unidad": "Código de unidad curricular",
            "nombre": "Nombre de unidad",
            "area_de_conocimiento": "Áreas de conocimiento",
            "horas_totales": "Horas totales",
            "horas_semanales": "Horas semanales",
            "horas_sincronicas": "Horas sincrónicas",
            "horas_asincronicas": "Horas asincrónicas",
            "tipo_de_componente": "Tipo de componente",
            "criterio_de_aprobacion": "Nota mínima de aprobación",
            "porcentaje_minimo_asistencia": "Porcentaje mínimo de asistencia (%)",
        }

    def clean(self):
        #Validación de horas totales.
        registros = super().clean()
        horas_sincronicas = registros.get("horas_sincronicas", 0)
        horas_asincronicas = registros.get("horas_asincronicas", 0)
        horas_totales = registros.get("horas_totales", 0)
        if horas_sincronicas and horas_asincronicas and horas_totales:
            if (horas_sincronicas + horas_asincronicas) != horas_totales:
                raise forms.ValidationError(
                    f"Las horas registradas deben coincidir con el total de {horas_totales} horas."
                )
        return registros


#Periodo de nivelación
class FormularioPeriodoDeNivelacion(forms.ModelForm):
    class Meta:
        model = PeriodoDeNivelacion
        fields = ("universidad", "codigo_periodo", "anio", "periodo", "fecha_inicio", "fecha_fin", "modalidad", "numero_periodo")
        labels = {
            "universidad": "Universidad",
            "codigo_periodo": "Código de periodo",
            "anio": "Año",
            "periodo": "Periodo",
            "fecha_inicio": "Fecha de inicio",
            "fecha_fin": "Fecha de fin",
            "modalidad": "Modalidad",
            "numero_periodo": "Número de periodo",
        }
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin"   : forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        #Validación de que fechas
        registros = super().clean()
        fecha_inicio = registros.get("fecha_inicio")
        fecha_fin = registros.get("fecha_fin")
        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise forms.ValidationError(
                "La fecha de fin debe ser posterior a la fecha de inicio."
            )
        return registros


#Paralelo
class FormularioParalelo(forms.ModelForm):
    class Meta:
        model = Paralelo
        fields = ("periodo_de_nivelacion", "unidad_curricular", "codigo_de_paralelo", "nombre", "jornada", "modalidad", "capacidad_maxima", "docente_responsable")
        labels = {
            "periodo_de_nivelacion": "Periodo de nivelación",
            "unidad_curricular": "Unidad curricular",
            "codigo_de_paralelo": "Código de paralelo",
            "nombre": "Nombre de paralelo",
            "jornada": "Jornada",
            "modalidad": "Modalidad",
            "capacidad_maxima": "Capacidad máxima",
            "docente_responsable": "Docente responsable",
        }


#Horario
class FormularioHorario(forms.ModelForm):
    class Meta:
        model  = Horario
        fields = ("paralelo", "dia_semana", "hora_inicio", "hora_fin", "espacio_de_imparticion", "modalidad", "numero_semana", "tipo_de_sesion")
        labels = {
            "paralelo": "Paralelo",
            "dia_semana": "Día de la semana",
            "hora_inicio": "Hora de inicio",
            "hora_fin": "Hora de fin",
            "espacio_de_imparticion": "Espacio de impartición",
            "modalidad": "Modalidad",
            "numero_semana": "Número de semana",
            "tipo_de_sesion": "Tipo de sesión",
        }
        widgets = {
            "hora_inicio": forms.TimeInput(attrs = {"type": "time"}),
            "hora_fin"   : forms.TimeInput(attrs = {"type": "time"}),
        }

    def clean(self):
        #Validar horas
        registros = super().clean()
        hora_inicio = registros.get("hora_inicio")
        hora_fin = registros.get("hora_fin")
        if hora_inicio and hora_fin and hora_fin <= hora_inicio:
            raise forms.ValidationError(
                "La hora de fin debe ser posterior a la hora de inicio."
            )
        return registros


#Cohorte de matrícula
class FormularioCohorteDeMatricula(forms.ModelForm):
    class Meta:
        model = CohorteDeMatricula
        fields = ("periodo_de_nivelacion", "codigo_de_registro", "fecha_de_cierre", "tipo_de_cohorte")
        labels = {
            "periodo_de_nivelacion": "Periodo de nivelación",
            "codigo_de_registro": "Código de registro",
            "fecha_de_cierre": "Fecha de cierre",
            "tipo_de_cohorte": "Tipo de cohorte",
        }
        widgets = {
            "fecha_de_cierre": forms.DateInput(attrs = {"type": "date"})
        }


#Evaluación académica
class FormularioEvaluacionAcademica(forms.ModelForm):
    class Meta:
        model = EvaluacionAcademica
        fields = ("estudiante", "unidad_curricular", "calificacion_parcial_1", "calificacion_parcial_2", "porcentaje_asistencia", "observacion")
        labels = {
            "estudiante": "Estudiante",
            "unidad_curricular": "Unidad curricular",
            "calificacion_parcial_1": "Calificación parcial 1",
            "calificacion_parcial_2": "Calificación parcial 2",
            "porcentaje_asistencia": "Porcentaje de asistencia (%)",
            "observacion": "Observación",
        }

    def clean_calificacion_parcial_1(self):
        calificacion = self.cleaned_data.get("calificacion_parcial_1")
        if calificacion is not None and not (0.0 <= calificacion <= 10.0):
            raise forms.ValidationError("Calificación no válida (0.0 - 10.0).")
        return calificacion

    def clean_calificacion_parcial_2(self):
        calificacion = self.cleaned_data.get("calificacion_parcial_2")
        if calificacion is not None and not (0.0 <= calificacion <= 10.0):
            raise forms.ValidationError("Calificación no válida (0.0 - 10.0).")
        return calificacion

    def clean_porcentaje_asistencia(self):
        porcentaje = self.cleaned_data.get("porcentaje_asistencia")
        if porcentaje is not None and not (0.0 <= porcentaje <= 100.0):
            raise forms.ValidationError("Porcentaje no válido (0.0 - 100.0).")
        return porcentaje