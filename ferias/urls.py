from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_feria, name='registrar_feria'),
    path('listar/', views.listar_ferias, name='listar_ferias'),
]