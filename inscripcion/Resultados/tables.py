# tutorial/tables.py
import django_tables2 as tables
from .models import estadisticas

class estadisticas2(tables.Table):

    class Meta:
        model = estadisticas
        fields = ("equipos","jg","jp","puntos","gaf","gc","dif","faltas" )
        attrs = {"class": "mytable"}