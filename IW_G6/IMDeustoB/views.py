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

    if skills_ids:
        peliculas = Pelicula.objects.filter(generos__id__in=skills_ids)

    # Año más antiguo y más reciente
    anyoMenor = Pelicula.objects.order_by('anyo').first()
    anyoMayor = Pelicula.objects.order_by('anyo').last()

    lista_anyos = []
    if anyoMenor and anyoMayor:
        lista_anyos = list(range(anyoMenor.anyo, anyoMayor.anyo + 1))

    # Filtro por rango de años
    desde = request.GET.get('anyoMenor')
    hasta = request.GET.get('anyoMayor')

    if desde:
        peliculas = peliculas.filter(anyo__gte=desde)
    if hasta:
        peliculas = peliculas.filter(anyo__lte=hasta)

    return render(
        request,
        'index.html',
        {
            'peliculas': peliculas,
            'generos': generos,
            'lista_anyos': lista_anyos,
        }
    )
class PeliculaDetailView(DetailView):
    model = Pelicula
    context_object_name = 'pelicula'
    template_name = 'moviesingle.html'

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


'''

class GeneroListView(ListView)
    model = Genero #object_list
    context_object_name = "generos"
    template_name = 'el html'

    queryset = Liga.object.all().order_by("nombre")

    


'''
