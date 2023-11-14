from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tarefas.models import Tarefa


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("index"))

        self.assertEqual(str(response.context["user"]), "testuser")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")


class ListaTarefasViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()

        for i in range(1, 3):
            # Tarefas para o teste
            Tarefa.objects.create(
                usuario=test_user,
                titulo=f"Tarefa de teste {i}",
                descricao=f"Esta é a {i}ª tarefa de teste",
                prioridade="M",
                data=f"{date.today() + timedelta(days=i)}",
                realizada=False,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("lista_tarefas"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/lista_tarefas/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("lista_tarefas"))
        self.assertEqual(str(response.context["user"]), "testuser")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lista_tarefas.html")

    def test_no_tarefas_in_context_if_no_match(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("lista_tarefas") + "?titulo=Nonexistent")
        self.assertEqual(len(response.context["tarefas"]), 0)

    def test_tarefas_in_context_if_match(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("lista_tarefas") + "?titulo=teste")
        self.assertEqual(len(response.context["tarefas"]), 2)


class AdicionarTarefaViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("adicionar_tarefa"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/adicionar_tarefa/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("adicionar_tarefa"))

        self.assertEqual(str(response.context["user"]), "testuser")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form_tarefa.html")

    def test_form_with_valid_post(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("adicionar_tarefa"),
            {
                "titulo": "Tarefa de teste",
                "descricao": "Esta é uma tarefa de teste",
                "prioridade": "M",
                "data": date.today(),
                "realizada": False,
            },
        )
        self.assertEqual(response.status_code, 204)
        # Verifique se a tarefa foi adicionada corretamente
        self.assertEqual(Tarefa.objects.count(), 1)
        self.assertEqual(Tarefa.objects.get().titulo, "Tarefa de teste")

    def test_form_with_invalid_post(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("adicionar_tarefa"),
            {
                "titulo": "Ta",
                "descricao": "Es",
                "prioridade": "K",
                "data": date.today() - timedelta(days=1),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Certifique-se de que o título tenha no mínimo 3 caracteres.",
            response.content.decode(),
        )
        self.assertIn(
            "Certifique-se de que a descrição tenha no mínimo 3 caracteres.",
            response.content.decode(),
        )
        self.assertIn(
            "Faça uma escolha válida. K não é uma das escolhas disponíveis.",
            response.content.decode(),
        )
        self.assertIn(
            "Insira uma data a partir do dia atual.",
            response.content.decode(),
        )


class FinalizarTarefaViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()

        test_tarefa = Tarefa.objects.create(
            usuario=test_user,
            titulo="Tarefa de teste",
            descricao="Esta é uma tarefa de teste",
            prioridade="M",
            data="2023-11-13",
            realizada=False,
        )
        test_tarefa.save()

    def test_redirect_if_not_logged_in(self):
        tarefa = Tarefa.objects.get(id=1)
        response = self.client.get(reverse("finalizar_tarefa", args=[tarefa.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/finalizar_tarefa/1/")

    def test_logged_in_can_finalize_task(self):
        self.client.login(username="testuser", password="12345")
        tarefa = Tarefa.objects.get(id=1)
        response = self.client.get(reverse("finalizar_tarefa", args=[tarefa.id]))

        # Verifique se a tarefa foi finalizada corretamente
        tarefa.refresh_from_db()
        self.assertTrue(tarefa.realizada)


class EditarTarefaViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()

        test_tarefa = Tarefa.objects.create(
            usuario=test_user,
            titulo="Tarefa de teste",
            descricao="Esta é uma tarefa de teste",
            prioridade="M",
            data="2023-11-13",
            realizada=False,
        )
        test_tarefa.save()

    def test_redirect_if_not_logged_in(self):
        tarefa = Tarefa.objects.get(id=1)
        response = self.client.get(reverse("editar_tarefa", args=[tarefa.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/editar_tarefa/1/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="testuser", password="12345")
        tarefa = Tarefa.objects.get(id=1)
        response = self.client.get(reverse("editar_tarefa", args=[tarefa.id]))

        self.assertEqual(str(response.context["user"]), "testuser")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form_tarefa.html")

    def test_edit_form_with_valid_post(self):
        self.client.login(username="testuser", password="12345")
        tarefa = Tarefa.objects.get(id=1)
        response = self.client.post(
            reverse("editar_tarefa", args=[tarefa.id]),
            {
                "titulo": "Tarefa atualizada",
                "descricao": "Esta é uma tarefa de teste atualizada",
                "prioridade": "A",
                "data": date.today(),
            },
        )
        self.assertEqual(response.status_code, 204)
        # Verifique se a tarefa foi atualizada corretamente
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.titulo, "Tarefa atualizada")
        self.assertEqual(tarefa.descricao, "Esta é uma tarefa de teste atualizada")
        self.assertEqual(tarefa.prioridade, "A")
        self.assertEqual((tarefa.data), date.today())

    def test_edit_form_with_invalid_post(self):
        self.client.login(username="testuser", password="12345")
        tarefa = Tarefa.objects.get(id=1)
        response = self.client.post(
            reverse("editar_tarefa", args=[tarefa.id]),
            {
                "titulo": "Ta",
                "descricao": "Es",
                "prioridade": "K",
                "data": date.today() - timedelta(days=1),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Certifique-se de que o título tenha no mínimo 3 caracteres.",
            response.content.decode(),
        )
        self.assertIn(
            "Certifique-se de que a descrição tenha no mínimo 3 caracteres.",
            response.content.decode(),
        )
        self.assertIn(
            "Faça uma escolha válida. K não é uma das escolhas disponíveis.",
            response.content.decode(),
        )
        self.assertIn(
            "Insira uma data a partir do dia atual.",
            response.content.decode(),
        )


class ExcluirTarefaViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()

        test_tarefa = Tarefa.objects.create(
            usuario=test_user,
            titulo="Tarefa de teste",
            descricao="Esta é uma tarefa de teste",
            prioridade="M",
            data=date.today(),
            realizada=False,
        )
        test_tarefa.save()

    def test_redirect_if_not_logged_in(self):
        tarefa = Tarefa.objects.get(id=1)
        response = self.client.delete(reverse("excluir_tarefa", args=[tarefa.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/excluir_tarefa/1/")

    def test_logged_in_can_delete_task(self):
        self.client.login(username="testuser", password="12345")
        tarefa = Tarefa.objects.get(id=1)
        response = self.client.delete(reverse("excluir_tarefa", args=[tarefa.id]))
        self.assertEqual(response.status_code, 204)
        # Verifique se a tarefa foi excluída corretamente
        self.assertFalse(Tarefa.objects.filter(id=1).exists())
