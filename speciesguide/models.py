import os
import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import djgeojson.fields as geofields
from django.utils.text import slugify


# Create your models here.

class Month(models.Model):
    name = models.CharField(max_length=10)
    abbr_name = models.CharField(max_length=3)
    number = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(12)])
    
    def __str__(self):
        return self.name


class State(models.Model):
    name=models.CharField(max_length=50)
    short = models.CharField(max_length=2)
    def __str__(self):
        return "{} - {}".format(self.name,self.short)


class Habitat(models.Model):
    slug = models.CharField(max_length=50)
    def __str__(self):
        return self.slug


class Family(models.Model):
    name = models.CharField(max_length=50, verbose_name="Família")
    slug = models.SlugField()
    description = models.TextField(verbose_name="Descrição")
    thematic_hexacolor = models.CharField(max_length=7, verbose_name="Cor Temática", help_text="cor temática da família, em hexadecimal")
    symbol = models.FilePathField()
    class Meta:
        verbose_name_plural="Families"    
         
    def save(self, *args, **kwargs):
        super(Family, self).save(*args, **kwargs)
        self.slug=slugify(self.name)
        super(Family, self).save(*args, **kwargs)
           
    def __str__(self):
        return self.name


class Species(models.Model):
    """
    Tamanho:
    Hábito: 
    Remove abundancia
    Melhorar hábito
    Adicionar período reprodutivo, épocas de vocalização e de girinos
        
    """
    def thumb(self):
        try:
            return self.media.filter(sp_prof_img=True)[0].file.url
        except:
            return "http://placehold.it/800x450"
    
    ACTIVITY_TIMING_CHOICES = (
        ('DIUR', 'Diurno'),
        ('NOCT', 'Noturno'),    
    )
    

    name = models.CharField(max_length=50, verbose_name="Nome científico")
    vernacular = models.CharField(max_length=100, verbose_name="Nome Comum")
    slug = models.SlugField()
    description = models.TextField(verbose_name="Descrição")
    family = models.ForeignKey(Family, verbose_name="Família")
    size = models.FloatField(verbose_name="Tamanho", help_text="Insira o tamanho médio em centímetros")
    activity_timing = models.CharField(max_length=4,
                                       choices = ACTIVITY_TIMING_CHOICES,
                                       default = None)
    habitat = models.ManyToManyField(Habitat)
    occurrence_states = models.ManyToManyField(State, verbose_name="Estados de Ocorrência")
    occurrence_months = models.ManyToManyField(Month, related_name="month_occurring_species", verbose_name="Meses de Ocorrência")
    
    class Meta:
        verbose_name_plural = "Species"
        
    def save(self, *args, **kwargs):
        super(Species, self).save(*args, **kwargs)
        self.slug=slugify(self.name)
        super(Species, self).save(*args, **kwargs)
        
    def __str__(self):
        return "{0} ({1})".format(self.vernacular, self.name)
    


def sp_media_dirpath(instance, filename):  
    # upload media asset to MEDIA ROOT/species_<id>/<filename>  
    return 'sp_archive/{0}/{1}/{2}'.format(instance.type, instance.species.name.replace(" ","_").lower(), filename)

class MediaAsset(models.Model):
    
    def datetimeFromFile(self, file):
        datetime.datetime.fromtimestamp(os.path.getmtime(file))
        
    def image_thumb(self):
        return '<img src="%s" width="100" height="100" />' %(self.file.url)   
    image_thumb.allow_tags=True
    
    MEDIA_TYPES_CHOICES = [
        ('PICT', 'Fotografia'),
        ('VIDS', 'Vídeo'),
        ('SOUN', 'Audio'),
    ]
    file = models.FileField(upload_to=sp_media_dirpath, verbose_name="Arquivo")
    species = models.ForeignKey(Species, verbose_name="Espécie", related_name='media')
    type = models.CharField(max_length=5,
                            choices = MEDIA_TYPES_CHOICES,
                            default = None, verbose_name="Tipo")
    datetime = models.DateTimeField(verbose_name="DataHorário")  
    copyright = models.CharField(max_length=50, verbose_name="Autoria")
    description = models.TextField(verbose_name="Descrição")
    location = geofields.PointField(help_text=" ", verbose_name="Localidade") 
    sp_prof_img = models.BooleanField(verbose_name="Foto-perfil", help_text="Esta é a foto-perfil da espécie", default=False)
     
    def __str__(self):
        return self.file.name

class Article(models.Model):
    species = models.ManyToManyField(Species, related_name='articles')
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    ordering = models.IntegerField()
    def __str__(self):
        return self.slug
    