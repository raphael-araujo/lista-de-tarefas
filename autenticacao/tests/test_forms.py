from django.contrib.auth.models import User
from django.test import TestCase

from autenticacao.forms import CadastroForm, LoginForm


class CadastroFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="raphael", password="Password123", email="raphael@mail.com"
        )

    def test_cadastro_form_valid(self):
        form = CadastroForm(
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "Newpassword123",
                "password2": "Newpassword123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_cadastro_form_username_exists(self):
        form = CadastroForm(
            {
                "username": "raphael",
                "email": "newuser@example.com",
                "password1": "Newpassword123",
                "password2": "Newpassword123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"], ["Este nome de usuário já existe"])

    def test_cadastro_form_email_exists(self):
        form = CadastroForm(
            {
                "username": "newuser",
                "email": "raphael@mail.com",
                "password1": "Newpassword123",
                "password2": "Newpassword123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["Este e-mail já está cadastrado."])

    def test_cadastro_form_password_mismatch(self):
        form = CadastroForm(
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "newpassword123",
                "password2": "wrongpassword123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"], ["As senhas não coincidem"])


class LoginFormTest(TestCase):
    def test_login_form_valid(self):
        form = LoginForm(
            {
                "userinput": "testuser",
                "password": "testpassword123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_login_form_userinput_empty(self):
        form = LoginForm(
            {
                "userinput": "",
                "password": "testpassword123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["userinput"], ["Este campo é obrigatório."])

    def test_login_form_password_empty(self):
        form = LoginForm(
            {
                "userinput": "testuser",
                "password": "",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password"], ["Este campo é obrigatório."])
