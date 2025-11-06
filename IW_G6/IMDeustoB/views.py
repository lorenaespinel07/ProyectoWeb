from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from.models import Genero, Pelicula, Actor

# Create your views here.

def index(request):
    return render(request, 'index.html')


def lista_generos(request):
    generos= Genero.objects.all() 
    return render(request, 'lista_generos.html', {'generos': generos})


def detalle_generos(request, pk):
    genero = get_object_or_404(Genero, pk=pk)
    return render(request, 'detalle_generos.html', {'genero': genero})


def lista_peliculas(request):


    peliculas= Pelicula.objects.all() 
    return render(request, 'lista_peliculas.html', {'peliculas': peliculas})


def detalle_peliculas(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    return render(request, 'detalle_peliculas.html', {'pelicula': pelicula})


def lista_actores(request):
    actores = Actor.objects.all() 
    return render(request, 'lista_actores.html', {'actores': actores})


def detalle_actores(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    return render(request, 'detalle_actores.html', {'actor': actor})