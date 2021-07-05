from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Evento

# User Methods
def login_user(request: HttpRequest) -> HttpResponse:
    return render(request, 'login.html')

def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect('/')

def submit_user(request: HttpRequest) -> HttpResponseRedirect:
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

# Event Methods
@login_required(login_url='/login/')
def get_all_events(request: HttpRequest) -> HttpResponse:
    user = request.user
    events = Evento.objects.filter(usuario=user)
    
    return render(request, 'agenda.html', {
        'events': events,
        'user': user
    })

def get_event_by_title(request: HttpRequest, titulo_evento: str) -> HttpResponse:
    event = Evento.objects.get(titulo=titulo_evento)

    return HttpResponse(f'<h1>{event.titulo} = {event.data_evento}</h1>')

@login_required(login_url='/login/')
def create_event(request: HttpRequest) -> HttpResponse:
    event_id = request.GET.get('id')
    data = {}
    
    if event_id:
        data['event'] = Evento.objects.get(id=event_id)
    
    return render(request, 'evento.html', data)

@login_required(login_url='/login/')
def submit_event(request: HttpRequest) -> HttpResponseRedirect:
    if request.POST:
        event_id = request.POST.get('event_id')
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        usuario = request.user
        
        if event_id:
            event = Evento.objects.get(id=event_id)
            
            if event.usuario == usuario:
                Evento.objects.filter(id=event_id).update(
                titulo=titulo,
                descricao=descricao,
                data_evento=data_evento,
                local=local,
                usuario=usuario
            )
        else:
            Evento.objects.create(
                titulo=titulo,
                descricao=descricao,
                data_evento=data_evento,
                local=local,
                usuario=usuario
            )

    return redirect('/')

@login_required(login_url='/login/')
def delete_event(request: HttpRequest, id_evento: int) -> HttpResponseRedirect:
    user = request.user
    event = Evento.objects.get(id=id_evento)
    
    if user == event.usuario:
        event.delete()
    
    return redirect('/')
