import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import TarefaForm
from .models import Tarefa


def index(request: HttpRequest) -> HttpResponse:
    prioridades = [prioridade for prioridade in Tarefa.CHOICE_PRIORIDADE]
    return render(request, "index.html", {"prioridades": prioridades})


def lista_tarefas(request: HttpRequest) -> HttpResponse:
    filtro_titulo = request.GET.get("titulo")
    filtro_prioridade = request.GET.get("prioridade")
    tarefas = Tarefa.objects.filter(realizada=False).order_by("data")

    if filtro_titulo:
        tarefas = tarefas.filter(titulo__icontains=filtro_titulo)
    if filtro_prioridade:
        tarefas = tarefas.filter(prioridade=filtro_prioridade)

    return render(request, "lista_tarefas.html", {"tarefas": tarefas})


def adicionar_tarefa(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TarefaForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "taskListChanged": None,
                            "showMessage": "Tarefa adicionada com sucesso.",
                        }
                    )
                },
            )
    else:
        form = TarefaForm()

    return render(request, "form_tarefa.html", {"form": form})


def finalizar_tarefa(request: HttpRequest, id_tarefa: int) -> HttpResponse:
    tarefa = get_object_or_404(Tarefa, id=id_tarefa)
    tarefa.realizada = True
    tarefa.save()
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps(
                {
                    "taskListChanged": None,
                    "showMessage": "Tarefa finalizada com sucesso.",
                }
            )
        },
    )


def editar_tarefa(request: HttpRequest, id_tarefa: int) -> HttpResponse:
    tarefa = get_object_or_404(Tarefa, id=id_tarefa)

    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)

        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "taskListChanged": None,
                            "showMessage": "Tarefa atualizada com sucesso.",
                        }
                    )
                },
            )
    else:
        form = TarefaForm(instance=tarefa)

    return render(request, "form_tarefa.html", {"form": form, "tarefa": tarefa})


@require_http_methods(["DELETE"])
def excluir_tarefa(request: HttpRequest, id_tarefa: int) -> HttpResponse:
    tarefa = get_object_or_404(Tarefa, id=id_tarefa)
    tarefa.delete()
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps(
                {
                    "taskListChanged": None, 
                    "showMessage": "Tarefa excluída com sucesso."
                }
            )
        },
    )
