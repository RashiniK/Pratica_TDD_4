from django.shortcuts import render, redirect
from core.forms import AgendaForm, LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from http.client import HTTPResponse
from django.http import JsonResponse, HttpResponseBadRequest
from core.models import Agenda

def login(request):
    if request.user.id is not None:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")
        context = {'acesso_negado': True}
        return render(request, 'login.html', {'form':form})
    return render(request, 'login.html', {'form':LoginForm()})

        
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')
    return redirect("home")


@login_required
def home(request):
    context = {}
    return render(request, 'index.html', context)



@login_required
def listar(request):
    agendas = Agenda.objects.all()
    contexto = {"agendas": agendas}
    return render(request, 'listar.html', contexto)

@login_required
def cadastrar(request):
    contexto = {}

    if request.method == "POST":
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()

        else:
            contexto['form'] = form

    return render(request, 'cadastrar.html', contexto)

@login_required
def deletar(request):
    contexto = {}
    if request.method == "POST":
        try:
            id = int(request.POST.get("id"))
            model = Agenda.objects.get(pk=id)
            model.delete()
        except Exception as e:
            contexto["erro"] = "Não foi possível deletar" , e

    contatos = Agenda.objects.all()
    contexto["contatos"] = contatos
    return render(request, 'deletar.html', contexto)

@login_required
def editar(request):
    contexto = {}

    if request.GET.get("id"):

        model = Agenda.objects.all()
        id =  request.GET.get("id")
        try:
            data = model.filter(id = id).values('id', 'nome_completo', 'telefone', 'email', "observacao")

            if (data):
                return JsonResponse(list(data), safe=False)
            else:
                raise Exception("Não foi possivel carregar contato")
        except Exception as e:
            return HttpResponseBadRequest(e)

    if request.method == "POST":
        contexto = {}
        try:
            id = int(request.POST.get("id"))
            model = Agenda.objects.get(pk=id)
            form = AgendaForm(request.POST, instance=model)
            if form.is_valid():
                form.save()
        except Exception as e:
            contexto["error"]= "Não foi possível salver o contato"

    ids = Agenda.objects.all().values("id", "nome_completo")
    contexto["ids"] = ids

    return render(request, 'editar.html', contexto)