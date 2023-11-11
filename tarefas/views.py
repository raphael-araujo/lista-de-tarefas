import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import TarefaForm
from .models import Tarefa


@login_required(login_url="login")
def index(request: HttpRequest) -> HttpResponse:
    prioridades = [prioridade for prioridade in Tarefa.CHOICE_PRIORIDADE]
    return render(request, "index.html", {"prioridades": prioridades})


@login_required(login_url="login")
def lista_tarefas(request: HttpRequest) -> HttpResponse:
    filtro_titulo = request.GET.get("titulo")
    filtro_prioridade = request.GET.get("prioridade")
    tarefas = Tarefa.objects.filter(usuario=request.user, realizada=False).order_by("data")

    if filtro_titulo:
        tarefas = tarefas.filter(titulo__icontains=filtro_titulo)
    if filtro_prioridade:
        tarefas = tarefas.filter(prioridade=filtro_prioridade)

    return render(request, "lista_tarefas.html", {"tarefas": tarefas})


@login_required(login_url="login")
def adicionar_tarefa(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TarefaForm(request.POST)

        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user
            tarefa.save()
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


@login_required(login_url="login")
def finalizar_tarefa(request: HttpRequest, id_tarefa: int) -> HttpResponse:
    tarefa = get_object_or_404(Tarefa, id=id_tarefa, usuario=request.user)
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


@login_required(login_url="login")
def editar_tarefa(request: HttpRequest, id_tarefa: int) -> HttpResponse:
    tarefa = get_object_or_404(Tarefa, id=id_tarefa, usuario=request.user)

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


@login_required(login_url="login")
@require_http_methods(["DELETE"])
def excluir_tarefa(request: HttpRequest, id_tarefa: int) -> HttpResponse:
    tarefa = get_object_or_404(Tarefa, id=id_tarefa, usuario=request.user)
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
