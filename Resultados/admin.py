from django.contrib import admin
from . models import deporte,equipo,estadisticas,jugador,categoria,rama, partidos

admin.site.register(deporte)
admin.site.register(rama)
admin.site.register(categoria)
admin.site.register(jugador)
admin.site.register(estadisticas)
admin.site.register(equipo)
admin.site.register(partidos)


# Register your models here.
