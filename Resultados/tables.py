# tutorial/tables.py
import django_tables2 as tables
from .models import estadisticas
from django_tables2.export.views import ExportMixin
from django_filters import FilterSet

class estadisticas2(tables.Table, ExportMixin):
    export_formats = ['csv']

    class Meta:
        model = estadisticas
        fields = ("equipos","jg","jp","puntos","gaf","gc","dif","faltas" )
        attrs = {"class": "mytable"}
        order_by = ("-puntos",)

