# accounts/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Role, Permission
from .models import Role, Permission

User = get_user_model()

class BootstrapAuthenticationForm(AuthenticationForm):
    """
    Login accesible con Bootstrap 5:
    - Autocomplete correcto (username/current-password)
    - Lectura por lector de pantalla (aria-describedby)
    - Mejor UX (autocapitalize none, spellcheck off, placeholders claros)
    """
    error_messages = {
        "invalid_login": "Usuario o contraseña incorrectos.",
        "inactive": "Esta cuenta está desactivada.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Usuario"
        self.fields['username'].widget.attrs.update({
            "class": "form-control",
            "id": "id_username",
            "placeholder": "Ingresa tu usuario",
            "autocomplete": "username",
            "autocapitalize": "none",
            "spellcheck": "false",
            "inputmode": "text",
            "required": "required",
            "aria-describedby": "usernameHelp",
        })

        self.fields['password'].label = "Contraseña"
        self.fields['password'].widget.attrs.update({
            "class": "form-control",
            "id": "id_password",
            "placeholder": "Ingresa tu contraseña",
            "autocomplete": "current-password",
            "required": "required",
            "aria-describedby": "passwordHelp",
        })


class RegisterForm(UserCreationForm):
    """
    Registro accesible:
    - Autocomplete específico por campo
    - Placeholders y ayudas
    - Validación de email único
    """
    email = forms.EmailField(
        required=True,
        label="Correo",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "id": "id_email",
            "placeholder": "nombre@empresa.com",
            "autocomplete": "email",
            "inputmode": "email",
            "aria-describedby": "emailHelp",
        })
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Usuario"
        self.fields['username'].widget.attrs.update({
            "class": "form-control",
            "id": "id_username",
            "placeholder": "Elige un nombre de usuario",
            "autocomplete": "username",
            "autocapitalize": "none",
            "spellcheck": "false",
            "inputmode": "text",
            "aria-describedby": "usernameRegHelp",
        })

        self.fields['password1'].label = "Contraseña"
        self.fields['password1'].widget.attrs.update({
            "class": "form-control",
            "id": "id_password1",
            "placeholder": "Crea una contraseña segura",
            "autocomplete": "new-password",
            "aria-describedby": "password1Help",
        })

        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['password2'].widget.attrs.update({
            "class": "form-control",
            "id": "id_password2",
            "placeholder": "Repite la contraseña",
            "autocomplete": "new-password",
            "aria-describedby": "password2Help",
        })

        for name in ("username", "password1", "password2"):
            if self.fields[name].help_text:
                self.fields[name].help_text = None

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "roles",
        ]


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ["name", "description", "permissions"]


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ["name", "code", "description"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "roles",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "roles": forms.SelectMultiple(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_superuser": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ["name", "description", "permissions"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "permissions": forms.SelectMultiple(attrs={"class": "form-select"}),
        }


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ["name", "code", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
