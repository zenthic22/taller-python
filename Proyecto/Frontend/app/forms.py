from django import forms

class BannerForm(forms.Form):
    banner = forms.ImageField(
        label='Selecciona el nuevo banner',
        required=True,  # El campo es requerido para que el profesor suba una imagen
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

class CursoForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    codigo = forms.CharField(label='Código', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    costo = forms.DecimalField(label='Costo', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    horario = forms.CharField(label='Horario', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cupo = forms.IntegerField(label='Cupo', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    catedratico_id = forms.IntegerField(label='ID del Catedrático', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    mensaje_bienvenida = forms.CharField(label='Mensaje de Bienvenida', widget=forms.Textarea(attrs={'class': 'form-control'}))
    estado = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    banner = forms.FileField(label='Banner (opcional)', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    def clean_banner(self):
        banner = self.cleaned_data.get('banner')
        if banner:
            if banner.size > 2 * 1024 * 1024:  # Tamaño máximo de 2MB
                raise forms.ValidationError("El tamaño máximo permitido para el banner es de 2MB.")
        return banner

class RegistroCatedraticoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    apellido = forms.CharField(max_length=100, label='Apellido')
    DPI = forms.CharField(max_length=13, label='DPI')
    especialidad = forms.CharField(max_length=100, label='Especialidad')  # Nuevo campo
    password = forms.CharField(max_length=8, widget=forms.PasswordInput(), label='Contraseña')
    confirm_password = forms.CharField(max_length=8, widget=forms.PasswordInput(), label='Confirmación de Contraseña')

class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    DPI = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    telefono = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre_usuario = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(max_length=8, label='Confirmar contraseña', widget=forms.PasswordInput())

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control'}))