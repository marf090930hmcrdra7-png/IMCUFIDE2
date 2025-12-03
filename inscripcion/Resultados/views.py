from django.shortcuts import render

from django.shortcuts import render
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

def inicio(request):
    return render(request,'Inicio.html')

from .models import estadisticas
from .tables import estadisticas2

class PersonListView(SingleTableView, ExportMixin):
    model = estadisticas
    table_class = estadisticas2
    template_name = 'Tabla.html'


