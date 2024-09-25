from django import forms

class RegistroCatedraticoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    apellido = forms.CharField(max_length=100, label='Apellido')
    DPI = forms.CharField(max_length=20, label='DPI')
    especialidad = forms.CharField(max_length=100, label='Especialidad')  # Nuevo campo
    password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirmación de Contraseña')

class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    DPI = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    telefono = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre_usuario = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput())

    # Nuevo campo para seleccionar el rol
    ROL_CHOICES = [
        (1, 'Administrador'),
        (2, 'Catedrático'),  # Agregado
        (3, 'Estudiante'),
    ]
    rol = forms.ChoiceField(choices=ROL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))