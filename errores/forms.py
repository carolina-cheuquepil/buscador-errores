from django import forms
from django.db.models import Q

from .dominios.catalogos import Frecuencia, Prueba
from .dominios.errores import Error, ErrorSolucion
from .dominios.plataforma import Hardware, Sistema
from .dominios.soluciones import Departamento, DepartamentoContacto, Responsable, Solucion, SolucionAsignacion


class ErrorForm(forms.ModelForm):
    soluciones = forms.ModelMultipleChoiceField(
        queryset=Solucion.objects.all(),
        required=False,
        label='Soluciones',
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6}),
    )

    class Meta:
        model = Error
        fields = [
            'descripcion', 'imagen_error', 'usuario',
            'hardware', 'sistema', 'modulo',
            'causa', 'soluciones',
            'frecuencia', 'comentarios',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'imagen_error': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'usuario': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'hardware': forms.Select(attrs={'class': 'form-select'}),
            'sistema': forms.Select(attrs={'class': 'form-select'}),
            'modulo': forms.Select(attrs={'class': 'form-select'}),
            'causa': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'frecuencia': forms.Select(attrs={'class': 'form-select'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hardware_id = self.data.get('hardware') if self.is_bound else self.instance.hardware_id
        sistema_id = self.data.get('sistema') if self.is_bound else self.instance.sistema_id

        if hardware_id:
            sistemas = Sistema.objects.filter(hardware__id=hardware_id)
            if sistema_id:
                sistemas = Sistema.objects.filter(Q(id=sistema_id) | Q(hardware__id=hardware_id))
            self.fields['sistema'].queryset = sistemas.distinct()

        if self.instance.pk:
            self.fields['soluciones'].initial = Solucion.objects.filter(
                errorsolucion__error=self.instance,
            )

    def clean(self):
        cleaned_data = super().clean()
        hardware = cleaned_data.get('hardware')
        sistema = cleaned_data.get('sistema')
        modulo = cleaned_data.get('modulo')

        if hardware and sistema and not hardware.sistemas.filter(pk=sistema.pk).exists():
            self.add_error('sistema', 'El sistema seleccionado no está relacionado con el hardware.')
        if modulo and not sistema:
            self.add_error('sistema', 'Debe indicar un sistema si selecciona un modulo.')
        if sistema and modulo and modulo.sistema_id != sistema.id:
            self.add_error('modulo', 'El modulo debe pertenecer al sistema seleccionado.')

        return cleaned_data

    def save(self, commit=True):
        error = super().save(commit=commit)
        if commit:
            self._guardar_soluciones(error)
        return error

    def _guardar_soluciones(self, error):
        soluciones = self.cleaned_data.get('soluciones')
        solucion_ids = {solucion.id for solucion in soluciones}
        relaciones = ErrorSolucion.objects.filter(error=error)
        relaciones.exclude(solucion_id__in=solucion_ids).delete()
        existentes = set(relaciones.values_list('solucion_id', flat=True))
        ErrorSolucion.objects.bulk_create([
            ErrorSolucion(error=error, solucion=solucion)
            for solucion in soluciones
            if solucion.id not in existentes
        ])


class BusquedaForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar en descripcion, causa o solucion...',
            'autofocus': 'autofocus',
        })
    )
    hardware = forms.ModelChoiceField(
        queryset=Hardware.objects.all(),
        required=False,
        empty_label='Todos',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sistema = forms.ModelChoiceField(
        queryset=Sistema.objects.all(),
        required=False,
        empty_label='Todos',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    frecuencia = forms.ModelChoiceField(
        queryset=Frecuencia.objects.all(),
        required=False,
        empty_label='Todas',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class HardwareForm(forms.ModelForm):
    class Meta:
        model = Hardware
        fields = ['nombre', 'so', 'sistemas']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'so': forms.TextInput(attrs={'class': 'form-control'}),
            'sistemas': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
        }


class SistemaForm(forms.ModelForm):
    class Meta:
        model = Sistema
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DepartamentoForm(forms.ModelForm):
    responsables = forms.ModelMultipleChoiceField(
        queryset=Responsable.objects.filter(activo=True),
        required=False,
        label='Responsables',
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
    )

    class Meta:
        model = Departamento
        fields = ['nombre', 'activo', 'responsables']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['responsables'].queryset = Responsable.objects.filter(
                Q(activo=True) | Q(departamento=self.instance)
            ).distinct()
            self.fields['responsables'].initial = Responsable.objects.filter(
                departamento=self.instance,
            )

    def save(self, commit=True):
        departamento = super().save(commit=commit)
        if commit:
            self._guardar_responsables(departamento)
        return departamento

    def _guardar_responsables(self, departamento):
        responsables = self.cleaned_data.get('responsables')
        responsable_ids = {responsable.id for responsable in responsables}
        Responsable.objects.filter(departamento=departamento).exclude(
            id__in=responsable_ids,
        ).update(departamento=None)
        Responsable.objects.filter(id__in=responsable_ids).update(departamento=departamento)


class DepartamentoContactoForm(forms.ModelForm):
    class Meta:
        model = DepartamentoContacto
        fields = ['tipo', 'numero', 'activo']
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono, correo, anexo...'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


DepartamentoContactoFormSet = forms.inlineformset_factory(
    Departamento,
    DepartamentoContacto,
    form=DepartamentoContactoForm,
    extra=1,
    can_delete=True,
)


class ResponsableForm(forms.ModelForm):
    class Meta:
        model = Responsable
        fields = ['nombre', 'cargo', 'departamento', 'contacto', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PruebaForm(forms.ModelForm):
    class Meta:
        model = Prueba
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SolucionForm(forms.ModelForm):
    responsables = forms.ModelMultipleChoiceField(
        queryset=Responsable.objects.filter(activo=True),
        required=False,
        label='Responsables',
        widget=forms.CheckboxSelectMultiple,
    )
    departamentos = forms.ModelMultipleChoiceField(
        queryset=Departamento.objects.filter(activo=True),
        required=False,
        label='Departamentos',
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Solucion
        fields = ['nombre', 'pasos', 'anexos', 'responsables', 'departamentos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'pasos': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'anexos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['responsables'].queryset = Responsable.objects.filter(
                Q(activo=True) | Q(solucionasignacion__solucion=self.instance)
            ).distinct()
            self.fields['responsables'].initial = Responsable.objects.filter(
                solucionasignacion__solucion=self.instance,
            )
            self.fields['departamentos'].queryset = Departamento.objects.filter(
                Q(activo=True) | Q(solucionasignacion__solucion=self.instance)
            ).distinct()
            self.fields['departamentos'].initial = Departamento.objects.filter(
                solucionasignacion__solucion=self.instance,
            )

    def save(self, commit=True):
        solucion = super().save(commit=commit)
        if commit:
            self._guardar_asignaciones(solucion)
        return solucion

    def _guardar_asignaciones(self, solucion):
        responsables = self.cleaned_data.get('responsables')
        departamentos = self.cleaned_data.get('departamentos')
        SolucionAsignacion.objects.filter(solucion=solucion).delete()
        SolucionAsignacion.objects.bulk_create(
            [
                SolucionAsignacion(solucion=solucion, responsable=responsable)
                for responsable in responsables
            ] + [
                SolucionAsignacion(solucion=solucion, departamento=departamento)
                for departamento in departamentos
            ]
        )


class SolucionRapidaForm(SolucionForm):
    pass
