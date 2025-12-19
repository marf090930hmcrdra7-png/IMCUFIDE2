from django.shortcuts import render

from django.shortcuts import render
from django_tables2 import SingleTableView
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from . filters import categoriafilter
from django_tables2.views import SingleTableMixin
from . models import estadisticas, equipo, categoria

def inicio(request):
    return render(request,'Inicio.html')

from .models import estadisticas
from .tables import estadisticas2

class PersonListView(SingleTableView, ExportMixin):
    model = estadisticas
    table_class = estadisticas2
    template_name = 'Tabla.html'
    export_formats = 'csv'

def table_view(request):
    table = estadisticas2(estadisticas.objects.all())

    RequestConfig(request).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response(f"table.{export_format}")

    return render(request, "Tabla.html", {
        "table": table
    })


class CategoriaListView(SingleTableMixin, FilterView):
    table_class = estadisticas2
    model = estadisticas
    template_name = "Libre.html"
    filterset_class = categoriafilter
    context_object_name = 'Tabla'

    def get_queryset(self):
        # Aquí puedes elegir datos específicos
        return estadisticas.objects.filter(puntos__icontains=3)