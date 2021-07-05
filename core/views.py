from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Evento

def login_user(request: HttpRequest) -> HttpResponse:
    return render(request, 'login.html')

def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect('/')

def submit_login(request: HttpRequest) -> HttpResponseRedirect:
    if request.POST:
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,"Usuário ou Senha invalidos")
        
    return redirect('/')

def get_by_title(request: HttpRequest, titulo_evento: str) -> HttpResponse:
    event = Evento.objects.get(titulo=titulo_evento)

    return HttpResponse(f'<h1>{event.titulo} = {event.data_evento}</h1>')

@login_required(login_url='/login/')
def get_all(request: HttpRequest) -> HttpResponse:
    user = request.user
    events = Evento.objects.filter(usuario=user)
    
    return render(request, 'agenda.html', {
        'events': events,
    })

@login_required(login_url='/login/')
def create_evento(request: HttpRequest) -> HttpResponse:
    return render(request, 'evento.html')

@login_required(login_url='/login/')
def submit_evento(request: HttpRequest) -> HttpResponseRedirect:
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        
        Evento.objects.create(
            titulo=titulo,
            descricao=descricao,
            data_evento=data_evento,
            usuario=usuario
        )

    return redirect('/')
