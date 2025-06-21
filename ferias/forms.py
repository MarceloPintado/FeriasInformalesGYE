from django import forms
from .models import Feria

class FeriaForm(forms.ModelForm):
    servicios = forms.MultipleChoiceField(
        choices=Feria.SERVICIOS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Servicios Disponibles"
    )
    
    class Meta:
        model = Feria
        fields = [
            'id_feria', 'nombre_feria', 'fecha_inicio', 'fecha_fin',
            'horario', 'ubicacion', 'capacidad', 'tipo_feria',
            'costo_participacion', 'responsable', 'estado',
            'fecha_limite', 'forma_inscripcion', 'num_permisos',
            'servicios', 'normas', 'observaciones'
        ]
        
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'normas': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describa normas o requisitos...'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
            'id_feria': forms.TextInput(attrs={'required': True}),
            'nombre_feria': forms.TextInput(attrs={'required': True}),
            'ubicacion': forms.TextInput(attrs={'required': True}),
            'capacidad': forms.NumberInput(attrs={'required': True}),
            'responsable': forms.TextInput(attrs={'required': True}),
            'costo_participacion': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def clean_servicios(self):
        servicios = self.cleaned_data.get('servicios')
        if servicios:
            return ','.join(servicios)
        return ''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, convertir servicios de string a lista
        if self.instance.pk and self.instance.servicios:
            self.fields['servicios'].initial = self.instance.servicios.split(',')