import django_filters
from .models import estadisticas, categoria


class categoriafilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = estadisticas
        fields = ["pertenenciacategoria",]