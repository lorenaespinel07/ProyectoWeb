from django.db import models

# Create your models here.

class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Genero"
        verbose_name_plural = "Generos"

    def __str__(self):
        return self.nombre
    

class Pelicula(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    sinopsis = models.CharField(max_length=500, blank=True, null=True)
    anyo = models.PositiveIntegerField(blank=True, null=True)
    generos = models.ManyToManyField(Genero, null=True, blank=True, related_name="peliculas")
    imagen = models.URLField(blank=True, null=True)
    #actores

    class Meta:
        verbose_name = "Pelicula"
        verbose_name_plural = "Peliculas"

    def __str__(self):
        return self.nombre
    
class Actor(models.Model):
    nombre = models.CharField(max_length=100)
    nacimiento = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    imagen = models.URLField(blank=True, null=True)
    peliculas = models.ManyToManyField(Pelicula, null=True, blank=True, related_name="actores")

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actores"

    def __str__(self):
        return self.nombre



