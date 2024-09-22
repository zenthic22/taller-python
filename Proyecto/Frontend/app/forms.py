from django import forms

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
    rol_id = forms.ChoiceField(choices=[(1, 'Alumno'), (2, 'Catedrático'), (3, 'Administrador')])

class LoginForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))