from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [    
    path('',  cache_page(60 * 15)(views.lista_peliculas), name='lista_peliculas'),
    path('peliculas/<int:pk>/', views.PeliculaDetailView.as_view(), name='detalle_peliculas'),

    #path('actores/', views.lista_actores, name='lista_actores'),
    path('actores', cache_page(60 * 15)(views.ActorListView.as_view()), name='lista_actores'),
    path('actores/<int:pk>/', views.ActorDetailView.as_view(), name='detalle_actores'),

]
