from django.shortcuts import HttpResponse, render
from django.http.request import HttpRequest
from .models import Evento

def get_by_title(request: HttpRequest, titulo_evento: str) -> HttpResponse:
    event = Evento.objects.get(titulo=titulo_evento)

    return HttpResponse(f'<h1>{event.titulo} = {event.data_evento}</h1>')

def get_all(request: HttpRequest) -> HttpResponse:
    user = request.user
    events = Evento.objects.filter(usuario=user)
    
    return render(request, 'agenda.html', {
        'events': events,
    })
