from django.contrib import admin
from .models import Genero, Pelicula, Actor

# Register your models here.

admin.site.register(Genero)
admin.site.register(Pelicula)
admin.site.register(Actor)