from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CadastroForm(UserCreationForm):
    username = forms.CharField(label="username", min_length=5, max_length=150)
    email = forms.EmailField(label="email")
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        novo_usuario = User.objects.filter(username=username)
        if novo_usuario.count():
            raise ValidationError("Este nome de usuário já existe")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        novo_email = User.objects.filter(email=email)
        if novo_email.count():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data["username"],
            self.cleaned_data["email"],
            self.cleaned_data["password1"],
        )
        return user


class LoginForm(forms.Form):
    userinput = forms.CharField(label="userinput", min_length=5, max_length=150)
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    def clean_userinput(self):
        userinput = self.cleaned_data["userinput"]
        if len(userinput.strip()) == 0:
            raise ValidationError("Preencha este campo")
        return userinput

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password.strip()) == 0:
            raise ValidationError("Preencha este campo")
        return password
