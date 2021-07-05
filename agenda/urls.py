from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from core import views

urlpatterns = [
    path('', RedirectView.as_view(url='/eventos')),
    path('admin/', admin.site.urls),
    
    path('evento/<titulo_evento>', views.get_event_by_title),
    path('eventos/', views.get_all_events),
    path('eventos/create', views.create_event),
    path('eventos/submit', views.submit_event),
    path('eventos/delete/<int:id_evento>', views.delete_event),
    
    path('login/', views.login_user),
    path('login/submit', views.submit_user),
    path('logout/', views.logout_user)
]
