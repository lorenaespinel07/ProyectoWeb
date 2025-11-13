from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [    
    path('', views.lista_peliculas, name='lista_peliculas'),
    path('peliculas/<int:pk>/', views.PeliculaDetailView.as_view(), name='detalle_peliculas'),
    
    path('actores', views.ActorListView.as_view(), name='lista_actores'),
    path('actores/<int:pk>/', views.ActorDetailView.as_view(), name='detalle_actores'),

]