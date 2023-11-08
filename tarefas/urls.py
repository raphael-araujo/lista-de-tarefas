from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lista_tarefas/", views.lista_tarefas, name="lista_tarefas"),
    path("adicionar_tarefa/", views.adicionar_tarefa, name="adicionar_tarefa"),
    path("editar_tarefa/<int:id_tarefa>/", views.editar_tarefa, name="editar_tarefa"),
    path("finalizar_tarefa/<int:id_tarefa>/",views.finalizar_tarefa,name="finalizar_tarefa",),
    path("excluir_tarefa/<int:id_tarefa>/", views.excluir_tarefa, name="excluir_tarefa"),
]
