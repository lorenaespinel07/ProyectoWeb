from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from.models import Genero, Pelicula, Actor
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import requests


# Create your views here.

def lista_peliculas(request):
    response = requests.get("https://api.themoviedb.org/3/movie/popular?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES")
    resul = response.json()

    return render(
        request,
        'index.html',
        {
            'peliculas': resul['results'],
            'generos': None,
            'lista_anyos': None,
        }
    )
class PeliculaDetailView(DetailView):
    model = Pelicula
    context_object_name = 'pelicula'
    template_name = 'moviesingle.html'

    def get_queryset(self):
        peli_id = self.kwargs['pk'] 

        response = requests.get(f'https://api.themoviedb.org/3/movie/{peli_id}?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES')
        resul = response.json()
        # titulo, año, director, escritores, actores, generos, fecha, duracion, rating
        return 

def lista_actores(request):
    actores = Actor.objects.all()

    nombre = request.GET.get('nombre')
    letra = request.GET.get('letra')
    desde = request.GET.get('nacimientoDesde')
    hasta = request.GET.get('nacimientoHasta')
    
    # NOMBRE
    if nombre:
        actores = actores.filter(nombre__icontains=nombre)
    
    # LETRA INICIAL
    if letra:
        actores = actores.filter(nombre__istartswith=letra)
    
    # AÑO NACIMIENTO
    if desde or hasta:
        actores_filtrados = []
        for actor in actores:
            if actor.nacimiento and '/' in actor.nacimiento:
                try:
                    año_actor = int(actor.nacimiento.split('/')[2])
                    cumple_desde = not desde or año_actor >= int(desde)
                    cumple_hasta = not hasta or año_actor <= int(hasta)
                    if cumple_desde and cumple_hasta:
                        actores_filtrados.append(actor.id)
                except (ValueError, IndexError):
                    continue
        actores = Actor.objects.filter(id__in=actores_filtrados)
    
    actores_con_fecha = Actor.objects.exclude(nacimiento__isnull=True).exclude(nacimiento__exact='')
    
    años_nacimiento = []
    for actor in actores_con_fecha:
        if actor.nacimiento and '/' in actor.nacimiento:
            try:
                año = int(actor.nacimiento.split('/')[2])
                años_nacimiento.append(año)
            except (ValueError, IndexError):
                continue

    año_menor = min(años_nacimiento)
    año_mayor = max(años_nacimiento)
    lista_anyos_nacimiento = [str(año) for año in range(año_menor, año_mayor + 1)]


    return render(request, 'celebritylist.html', {
        'actores': actores,
        'lista_anyos_nacimiento': lista_anyos_nacimiento
    })

class ActorListView(ListView):
    model = Actor
    context_object_name = 'actores'
    template_name = "celebritylist.html"

class ActorDetailView(DetailView):
    model = Actor
    context_object_name = 'actor'
    template_name = 'celebritysingle.html' 

    # nombre, profesion (actor, productor, directo...), 
    # año de nacimiento, pais, altura
    def get_object(self):
        actor_id = self.kwargs["pk"]

        # Información de detalle del actor
        detalle = requests.get(
            f"https://api.themoviedb.org/3/person/{actor_id}?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES"
        ).json()

        return detalle
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actor_id = self.kwargs.get('pk') 

        # lista de pelis donde ha salido
        filmografia = requests.get(
            f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES"
        ).json()

        context['filmografia'] = filmografia

        return context
'''

class GeneroListView(ListView)
    model = Genero #object_list
    context_object_name = "generos"
    template_name = 'el html'

    queryset = Liga.object.all().order_by("nombre")

    


'''
