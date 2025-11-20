from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from.models import Genero, Pelicula, Actor
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


# Create your views here.

def lista_peliculas(request):
    peliculas= Pelicula.objects.all()
    generos = Genero.objects.all()

    idsGeneros = request.GET.getlist('skills')
    skills_ids = [int(skill) for skill in idsGeneros]

    anyoMenor = Pelicula.objects.order_by('anyo').first()
    anyoMayor = Pelicula.objects.order_by('anyo').last()

    if skills_ids:
        peliculas = Pelicula.objects.filter(generos__id__in=skills_ids)

    return render(request, 'index.html', {'peliculas': peliculas, 'generos': generos, 'anyoMenor': anyoMenor.anyo, 'anyoMayor': anyoMayor.anyo})

class PeliculaDetailView(DetailView):
    model = Pelicula
    context_object_name = 'pelicula'
    template_name = 'moviesingle.html'

class ActorListView(ListView):
    model = Actor
    context_object_name = 'actores'
    template_name = "celebritylist.html"

class ActorDetailView(DetailView):
    model = Actor
    context_object_name = 'actor'
    template_name = 'celebritysingle.html' 


'''

class GeneroListView(ListView)
    model = Genero #object_list
    context_object_name = "generos"
    template_name = 'el html'

    queryset = Liga.object.all().order_by("nombre")

    


'''