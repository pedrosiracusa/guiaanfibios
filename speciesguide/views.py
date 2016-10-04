from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, request
from django.views import generic
from .models import *
from .filters import *
from django.http.request import QueryDict
from django_filters.views import FilterView

# Create your views here.

def index(request):
    sp_list = Species.objects.order_by('species')
    context = {
        'sp_list': sp_list
    }
    return render(request, 'speciesguide/index.html', context)


class IndexView(generic.TemplateView):
    template_name = 'speciesguide/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['species'] = Species.objects.all()
        context['families'] = Family.objects.all()
        context['habitats'] = Habitat.objects.all()
        return context


class SpeciesListView(FilterView):
    template_name='speciesguide/species_list.html'
    context_object_name='species_list'
    filterset_class = SpeciesFilter
        
    def get_queryset(self):
        return Species.objects.order_by('vernacular')
    

    
class HabitatsListView(generic.ListView):
    template_name='speciesguide/habitat_list.html'
    context_object_name='habitat_list'
    def get_queryset(self):
        return Habitat.objects.order_by('name')


class SpeciesDetailView(generic.DetailView):
    template_name='speciesguide/species_detail.html'
    context_object_name='species_detail'
    def get_queryset(self):
        return Species.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(SpeciesDetailView, self).get_context_data(**kwargs)
        context['occurrence_states'] = context['species_detail'].occurrence_states.all() 
        context['articles'] = context['species_detail'].articles.all()
        context['months'] = Month.objects.all()
        self.getCompSizeToContext(context['species_detail'], context)
        return context
    
    def getCompSizeToContext(self, obj, context):
        """ Adds comparative species-hand size to context """
        handSize =  17 # average hand length, in cm
        renderSize = 80 # size to be rendered with, in px
        if obj.size > handSize:
            context['speciescompsize'] = renderSize
            context['handcompsize'] = (handSize/obj.size)*renderSize
        else:
            context['handcompsize'] = renderSize
            context['speciescompsize'] = (obj.size/handSize)*renderSize



class DetailView(generic.DetailView):
    model = Species
    #template_name = 'speciesguide/Species_detail.html'

def detail(request, sp_id):
    sp = get_object_or_404(Species, pk=sp_id)
    return render(request, 'speciesguide/detail.html', {'sp':sp } )

