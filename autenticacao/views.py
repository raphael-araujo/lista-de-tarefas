from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import CadastroForm, LoginForm

# Create your views here.


def cadastro(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            messages.success(request, "Usuário criado com sucesso.")
            return redirect(to="index")
    else:
        if request.user.is_authenticated:
            return redirect(to="index")
        form = CadastroForm()

    return render(request, "cadastro.html", {"form": form})


def login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            userinput = form.cleaned_data["userinput"]
            senha = form.cleaned_data["password"]

            # Login com username ou e-mail:
            try:
                user = User.objects.get(email=userinput)
                account = auth.authenticate(request, username=user.username, password=senha)

                if not account:
                    messages.error(request, message="login ou senha inválidos.")
                    return redirect(to="login")

                auth.login(request, account)
                return redirect(to="index")

            except:
                account = auth.authenticate(request, username=userinput, password=senha)

                if not account:
                    messages.error(request, message="login ou senha inválidos.")
                    return redirect(to="login")

                auth.login(request, account)
                return redirect(to="index")
    else:
        if request.user.is_authenticated:
            return redirect(to="index")
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect(to=login)
