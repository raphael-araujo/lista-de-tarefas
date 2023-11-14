from django.test import TestCase
from django.contrib.auth.models import User
from tarefas.models import Tarefa


class TarefaModelTest(TestCase):
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

    def test_titulo_label(self):
        tarefa = Tarefa.objects.get(id=1)
        field_label = tarefa._meta.get_field("titulo").verbose_name
        self.assertEqual(field_label, "titulo")

    def test_titulo_max_length(self):
        tarefa = Tarefa.objects.get(id=1)
        max_length = tarefa._meta.get_field("titulo").max_length
        self.assertEqual(max_length, 40)

    def test_descricao_label(self):
        tarefa = Tarefa.objects.get(id=1)
        field_label = tarefa._meta.get_field("descricao").verbose_name
        self.assertEqual(field_label, "descricao")

    def test_prioridade_label(self):
        tarefa = Tarefa.objects.get(id=1)
        field_label = tarefa._meta.get_field("prioridade").verbose_name
        self.assertEqual(field_label, "prioridade")

    def test_data_label(self):
        tarefa = Tarefa.objects.get(id=1)
        field_label = tarefa._meta.get_field("data").verbose_name
        self.assertEqual(field_label, "data")

    def test_realizada_label(self):
        tarefa = Tarefa.objects.get(id=1)
        field_label = tarefa._meta.get_field("realizada").verbose_name
        self.assertEqual(field_label, "realizada")

    def test_usuario_label(self):
        tarefa = Tarefa.objects.get(id=1)
        field_label = tarefa._meta.get_field("usuario").verbose_name
        self.assertEqual(field_label, "usuario")

    def test_object_name_is_titulo(self):
        tarefa = Tarefa.objects.get(id=1)
        expected_object_name = f"{tarefa.titulo}"
        self.assertEqual(expected_object_name, str(tarefa))

    def test_icon(self):
        tarefa = Tarefa.objects.get(id=1)
        self.assertIsNotNone(tarefa.icon())
