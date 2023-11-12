from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from autenticacao.forms import CadastroForm


class CadastroViewTest(TestCase):
    # username="raphael",
    # password="Password123",
    # email="raphael@mail.com"
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="raphael", password="Password123", email="raphael@mail.com"
        )

    def test_status_code_200(self):
        response = self.client.get(reverse("cadastro"))
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse("cadastro"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "cadastro.html")

    def test_renders_blank_form(self):
        response = self.client.get(reverse("cadastro"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cadastro.html")
        self.assertIsInstance(response.context["form"], CadastroForm)

    def test_cadastro_view_get_with_user_authenticated(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(reverse("cadastro"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_cadastro_view_get_unauthenticated(self):
        response = self.client.get(reverse("cadastro"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cadastro.html")

    def test_cadastro_with_valid_data(self):
        response = self.client.post(
            reverse("cadastro"),
            {
                "username": "newuser123",
                "email": "newuser@example.com",
                "password1": "123Testando",
                "password2": "123Testando",
            },
        )
        messages = list((m.message for m in get_messages(response.wsgi_request)))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))
        self.assertIn("Usuário criado com sucesso.", messages)
        self.assertTrue(User.objects.filter(username="newuser123").exists())

    def test_cadastro_with_empty_fields(self):
        response = self.client.post(
            reverse("cadastro"),
            {
                "username": "",
                "email": "newuser@example.com",
                "password1": "Password123",
                "password2": "",
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn("Este campo é obrigatório.", response.content.decode())
        self.assertFalse(User.objects.filter(email="newuser@example.com").exists())

    def test_cadastro_with_mismatched_passwords(self):
        response = self.client.post(
            reverse("cadastro"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "Password123",
                "password2": "Newpass12",
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn("As senhas não coincidem", response.content.decode())
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_cadastro_with_existing_username(self):
        response = self.client.post(
            reverse("cadastro"),
            {
                "username": "raphael",
                "email": "newuser@example.com",
                "password1": "Password123",
                "password2": "Password123",
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn("Este nome de usuário já existe", response.content.decode())

    def test_cadastro_with_existing_email(self):
        response = self.client.post(
            reverse("cadastro"),
            {
                "username": "newuser",
                "email": "raphael@mail.com",
                "password1": "Password123",
                "password2": "Password123",
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn("Este e-mail já está cadastrado.", response.content.decode())

    def test_cadastro_with_invalid_email(self):
        response = self.client.post(
            reverse("cadastro"),
            {
                "username": "newuser",
                "email": "invalidemail",
                "password1": "Password123",
                "password2": "Password123",
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn("Informe um endereço de email válido.", response.content.decode())
        self.assertFalse(User.objects.filter(email="invalidemail").exists())


class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="raphael", email="raphael@mail.com", password="Password123"
        )

    def test_status_code_200(self):
        response = self.client.get(reverse("login"))
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse("login"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_view_get_authenticated(self):
        self.client.login(username="raphael", password="Password123")
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_login_view_get_unauthenticated(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_with_valid_credentials(self):
        self.assertTrue(self.client.login(username="raphael", password="Password123"))

        response = self.client.post(
            reverse("login"), {"userinput": "raphael", "password": "Password123"}
        )
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_login_with_invalid_credentials(self):
        self.assertFalse(
            self.client.login(username="raphael", password="Password123wrong")
        )
        response = self.client.post(
            reverse("login"), {"userinput": "raphael", "password": "Password123wrong"}
        )
        messages = list((m.message for m in get_messages(response.wsgi_request)))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertIn("login ou senha inválidos.", messages)

    def test_login_with_email(self):
        self.assertTrue(self.client.login(username="raphael", password="Password123"))

        response = self.client.post(
            reverse("login"),
            {"userinput": "raphael@mail.com", "password": "Password123"},
        )
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))


class LogoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="raphael", password="Password123")

    def test_logout(self):
        self.client.login(username="raphael", password="Password123")
        response = self.client.get(reverse("logout"))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
