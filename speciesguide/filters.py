import django_filters
from .models import *
from django import forms
from django.forms.models import ModelForm
from django.contrib.admin.utils import help_text_for_field

# https://django-filter.readthedocs.org/en/latest/usage.html
# https://github.com/alex/django-filter/issues/292 <- help text not added by default

class SpeciesFilter(django_filters.FilterSet):
    family = django_filters.ModelChoiceFilter(queryset=Family.objects.all().order_by('name'), 
                                              label="Selecione a Família", 
                                              empty_label="Todas",
                                              widget=forms.Select(attrs={"onChange":'this.form.submit()',
                                                                         "class": 'form-control'
                                                                         })
                                              )     
    class Meta:
        model = Species
        fields = ['family',]
        