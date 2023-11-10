from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import CadastroForm

# Create your views here.


def cadastro(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário criado com sucesso.")
            return redirect(to="cadastro")
    else:
        if request.user.is_authenticated:
            return redirect(to="index")
        form = CadastroForm()

    return render(request, "cadastro.html", {"form": form})
