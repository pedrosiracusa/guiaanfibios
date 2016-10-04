from django.conf.urls import url
from django_filters.views import FilterView
from . import views

app_name = 'speciesguide'
urlpatterns = [
        #url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'especies/$', views.SpeciesListView.as_view(), name="species_list"),
        url(r'habitats/$', views.HabitatsListView.as_view(), name="habitats"),
        url(r'listaespecies/$', views.SpeciesListView.as_view(), name="specieslist"),
        url(r'(?P<slug>.*)/$', views.SpeciesDetailView.as_view(), name='species_detail'),
    ]