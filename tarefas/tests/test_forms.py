from datetime import date

from django.test import TestCase

from tarefas.forms import TarefaForm


class TarefaFormTest(TestCase):
    def test_form_valid_data(self):
        form = TarefaForm(
            data={
                "titulo": "Tarefa de teste",
                "descricao": "Esta é uma tarefa de teste",
                "prioridade": "M",
                "data": date.today(),
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = TarefaForm(
            data={
                "titulo": "Ta",
                "descricao": "E",
                "prioridade": "K",
                "data": "2023-11-10",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
        self.assertEqual(
            ["Certifique-se de que o título tenha no mínimo 3 caracteres."],
            form.errors["titulo"],
        )
        self.assertEqual(
            ["Certifique-se de que a descrição tenha no mínimo 3 caracteres."],
            form.errors["descricao"],
        )
        self.assertEqual(
            ["Faça uma escolha válida. K não é uma das escolhas disponíveis."],
            form.errors["prioridade"],
        )
        self.assertEqual(
            ["Insira uma data a partir do dia atual."],
            form.errors["data"],
        )
