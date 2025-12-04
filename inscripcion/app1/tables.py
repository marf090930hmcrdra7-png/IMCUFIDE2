# tutorial/tables.py
import django_tables2 as tables
from .models import estadisticas

class estadisticas2(tables.Table):
    export_formats = ['csv']

    class Meta:
        model = estadisticas
        template_name = "django_tables2/bootstrap.html"
        fields = ("equipo","jg","jp","puntos","gaf","gc","dif","faltas" )
        attrs = {"class": "mytable"}