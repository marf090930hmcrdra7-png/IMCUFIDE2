# tutorial/tables.py
import django_tables2 as tables
from .models import estadisticas

class estadisticas2(tables.Table):

    class Meta:
        model = estadisticas
        template_name = "django_tables2/bootstrap.html"
        fields = ("equipo","jg","jp","puntos","gaf","gc","dif","amonestaciones" )
        attrs = {"class": "mytable"}