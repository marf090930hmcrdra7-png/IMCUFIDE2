from django import forms
from .models import Equipo, Jugador, PagoInscripcion, Categoria

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'categoria', 'nombre_promotor', 'telefono_promotor', 
                  'email_promotor', 'logo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del equipo'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nombre_promotor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del promotor'
            }),
            'telefono_promotor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+52 123 456 7890'
            }),
            'email_promotor': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'nombre': 'Nombre del Equipo',
            'categoria': 'Categoría',
            'nombre_promotor': 'Nombre del Promotor',
            'telefono_promotor': 'Teléfono',
            'email_promotor': 'Correo Electrónico',
            'logo': 'Logo del Equipo (opcional)'
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Equipo.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un equipo con este nombre.")
        return nombre


class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'edad', 'telefono', 
                  'email', 'direccion', 'posicion', 'numero_camiseta', 
                  'documento_identidad', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '5',
                'max': '100'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+52 123 456 7890'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'posicion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'numero_camiseta': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '99',
                'placeholder': 'Número de camiseta'
            }),
            'documento_identidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de documento'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'edad': 'Edad',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico (opcional)',
            'direccion': 'Dirección (opcional)',
            'posicion': 'Posición',
            'numero_camiseta': 'Número de Camiseta',
            'documento_identidad': 'Documento de Identidad',
            'foto': 'Foto del Jugador (opcional)'
        }
    
    def __init__(self, *args, **kwargs):
        self.equipo = kwargs.pop('equipo', None)
        super().__init__(*args, **kwargs)
    
    def clean_numero_camiseta(self):
        numero = self.cleaned_data.get('numero_camiseta')
        if self.equipo:
            if Jugador.objects.filter(
                equipo=self.equipo, 
                numero_camiseta=numero
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este número de camiseta ya está ocupado en el equipo.")
        return numero


class PagoInscripcionForm(forms.ModelForm):
    class Meta:
        model = PagoInscripcion
        fields = ['monto', 'metodo_pago', 'referencia', 'comprobante', 'notas']
        widgets = {
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-control'
            }),
            'referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de referencia o transacción'
            }),
            'comprobante': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': True
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales (opcional)'
            })
        }
        labels = {
            'monto': 'Monto del Pago',
            'metodo_pago': 'Método de Pago',
            'referencia': 'Referencia/Número de Transacción',
            'comprobante': 'Comprobante de Pago',
            'notas': 'Notas Adicionales'
        }


class BuscarEquipoForm(forms.Form):
    buscar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre de equipo...'
        })
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + Equipo.ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class BuscarJugadorForm(forms.Form):
    buscar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre...'
        })
    )
    posicion = forms.ChoiceField(
        choices=[('', 'Todas las posiciones')] + Jugador.POSICION_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )