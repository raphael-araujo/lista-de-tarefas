# Generated by Django 4.2.6 on 2023-11-13 23:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0006_tarefa_usuario_alter_tarefa_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefa',
            name='titulo',
            field=models.CharField(max_length=40, validators=[django.core.validators.MinLengthValidator(limit_value=3, message='Certifique-se de que o título tenha no mínimo 3 caracteres.')]),
        ),
    ]
