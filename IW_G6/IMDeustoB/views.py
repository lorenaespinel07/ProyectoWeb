from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from.models import Genero, Pelicula, Actor
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import requests


# Create your views here.

def lista_peliculas(request):
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 20)

    try:
        page = int(page)
    except ValueError:
        page = 1
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 20
        
    response = requests.get("https://api.themoviedb.org/3/movie/popular?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES")
    resul = response.json()

    peliculas = resul['results'][:per_page]

    return render(
        request,
        'index.html',
        {
            'peliculas': resul['results'],
            'generos': None,
            'lista_anyos': None,
            'page': page,
            'per_page': per_page,
            'total_pages': resul.get('total_pages', 1)
        }
    )
class PeliculaDetailView(DetailView):
    model = Pelicula
    context_object_name = 'pelicula'
    template_name = 'moviesingle.html'

    def get_object(self):
        peli_id = self.kwargs['pk'] 

        url = f'https://api.themoviedb.org/3/movie/{peli_id}?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES'

        response = requests.get(url=url)
        resul = response.json()

        
        # titulo, año, director, escritores, actores, generos, fecha, duracion, rating
        return resul
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        peli_id = self.kwargs.get('pk') 

        url = f'https://api.themoviedb.org/3/movie/{peli_id}/credits?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES'

        print(url)

        creditResul = requests.get(url=url)
        resulCredit = creditResul.json()

        print(resulCredit)
        context['creditos'] = resulCredit

        return context


class ActorListView(ListView):
    model = Actor
    context_object_name = "actores"
    template_name = "celebritylist.html"

    def get_queryset(self):
        request = self.request

        # Petición API
        url = "https://api.themoviedb.org/3/person/popular?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES"
        data = requests.get(url).json()
        
        actores = data.get("results", [])

        # 3. Obtener detalles del actor
        for actor in actores:
            detalle_url = f"https://api.themoviedb.org/3/person/{actor['id']}?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES"
            detalle_data = requests.get(detalle_url).json()
            actor["detalle"] = detalle_data

        return actores


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
