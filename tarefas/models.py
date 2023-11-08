from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.safestring import mark_safe


def validate_data(data: date):
    if data < date.today():
        raise ValidationError("Insira uma data a partir do dia atual.")


class Tarefa(models.Model):
    CHOICE_PRIORIDADE = (("B", "Baixa"), ("M", "Média"), ("A", "Alta"))

    titulo = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(
                limit_value=3,
                message="Certifique-se de que o título tenha no mínimo 3 caracteres.",
            )
        ],
    )
    descricao = models.TextField(
        max_length=50,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(
                limit_value=3,
                message="Certifique-se de que a descrição tenha no mínimo 3 caracteres.",
            )
        ],
    )
    prioridade = models.CharField(max_length=1, choices=CHOICE_PRIORIDADE)
    data = models.DateField(validators=[validate_data])
    realizada = models.BooleanField(default=False)

    def icon(self):
        if self.prioridade == "B":
            classe = "prioridade-verde"
        elif self.prioridade == "M":
            classe = "prioridade-amarelo"
        elif self.prioridade == "A":
            classe = "prioridade-vermelho"

        icon = f"""<svg  class="{classe}" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-triangle-fill" viewBox="0 0 16 16">
                                    <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                    </svg>"""

        return mark_safe(icon)

    def __str__(self):
        return self.titulo
