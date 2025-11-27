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

    print(resul)

    return render(
        request,
        'index.html',{'peliculas': resul['results'], 'pags_totales': resul['total_pages'], 'peliculas_totales': resul['total_results']}
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


        creditResul = requests.get(url=url)
        resulCredit = creditResul.json()

        context['creditos'] = resulCredit

        return context




class ActorListView(ListView):
    model = Actor
    context_object_name = "actores"
    template_name = "celebritylist.html"

    def get_queryset(self):

        request = self.request

        nombre = request.GET.get('nombre')
        letra = request.GET.get('letra')
        desde = request.GET.get('nacimientoDesde')
        hasta = request.GET.get('nacimientoHasta')

        # ------------------------------
        # 1. Petición base a TMDB
        # ------------------------------
        if nombre:
            url = "https://api.themoviedb.org/3/search/person?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES"
        else:
            url = "https://api.themoviedb.org/3/person/popular?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES"


        response = requests.get(url)
        data = response.json()

        actores = data.get("results", [])

        # ------------------------------
        # 2. Filtrar por letra inicial
        # ------------------------------
        if letra:
            actores = [
                a for a in actores
                if a["name"].lower().startswith(letra.lower())
            ]

        # ------------------------------
        # 3. Obtener detalles (cumpleaños)
        # ------------------------------
        actores_cumpleaños = []

        for actor in actores:
            detalle_url = f"https://api.themoviedb.org/3/person/{actor['id']}?api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES"
            detalle_resp = requests.get(detalle_url)
            detalle = detalle_resp.json()

            cumpleaños = detalle.get("birthday")  # YYYY-MM-DD o None

            actor["cumpleanyos"] = cumpleaños
            actores_cumpleaños.append(actor)

        # ------------------------------
        # 4. Filtrar por año de nacimiento
        # ------------------------------
        if desde or hasta:
            filtrados = []
            for actor in actores_cumpleaños:
                if actor["cumpleanyos"]:
                    try:
                        año = int(actor["cumpleanyos"].split("-")[0])  # YYYY
                        cumple_desde = not desde or año >= int(desde)
                        cumple_hasta = not hasta or año <= int(hasta)
                        if cumple_desde and cumple_hasta:
                            filtrados.append(actor)
                    except:
                        pass
            actores_cumpleaños = filtrados
        print(detalle_url)
        return actores_cumpleaños

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        actores = context["actores"]

        años = []
        for a in actores:
            if a["cumpleanyos"]:
                try:
                    años.append(int(a["cumpleanyos"].split("-")[0]))  # Usar YYYY
                except:
                    pass

        if años:
            context["lista_anyos_nacimiento"] = [
                str(a) for a in range(min(años), max(años) + 1)
            ]
        else:
            context["lista_anyos_nacimiento"] = []

        return context

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

