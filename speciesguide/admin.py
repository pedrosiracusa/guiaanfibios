from django.contrib import admin
from .models import *

from leaflet.admin import LeafletGeoAdmin

from django.utils.html import format_html
from django.forms import SelectMultiple
# Register your models here.


class MediaAssetAdmin(LeafletGeoAdmin):  
        
    def editAsset(self, obj):
        return "Editar"
    editAsset.short_description=''
    
    def thumb(self, obj):
        return format_html('<a href={}><img src="{}" width="100" height="100"/></a>', obj.file.url, obj.file.url)
    thumb.short_description = "Mídia"
    
    readonly_fields = ('image_thumb',)
    list_display = ('editAsset', 'thumb', 'description', 'species', 'datetime', 'type')   
    list_display_links = ('editAsset',)
    list_filter = ('type','species')
    fieldsets =[
        ('Mídia', {'fields': ['image_thumb', 'file', 'sp_prof_img']}),
        ('Meta', {'fields': ['type', 'datetime','species', 'copyright','description', 'location']})
    ]

    
    
class SpeciesAdmin(admin.ModelAdmin):
        
    fieldsets=[
        ('Espécie', {'fields': ['family', 'name', 'vernacular'] }),       
        ('Características Gerais', {'fields':['description', 'size', 'activity_timing','habitat'] }),
        ('Ocorrência', {'fields': ['occurrence_states', 'occurrence_months'] }),
    ]
    list_display = ('vernacular', 'name', 'family')
    search_fields = ['name']
    list_filter = ('family',)
    formfield_overrides = {models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': '10'})}, }
 
admin.site.register(Species, SpeciesAdmin)
admin.site.register(MediaAsset, MediaAssetAdmin)
admin.site.register(Habitat)
admin.site.register(Family)  
admin.site.register(Article)