from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('generos', views.lista_generos, name='lista_generos'),
    path('generos/<int:pk>/', views.detalle_generos, name='detalle_generos'),
    
    path('peliculas', views.lista_peliculas, name='lista_peliculas'),
    path('peliculas/<int:pk>/', views.detalle_peliculas, name='detalle_peliculas'),
    
    path('actores', views.lista_actores, name='lista_actores'),
    path('actores/<int:pk>/', views.detalle_actores, name='detalle_actores'),

    '''

        path('actores/<int:pk>/', views.GeneroListView.as_view(), name='detalle_actores')

    
    '''
]