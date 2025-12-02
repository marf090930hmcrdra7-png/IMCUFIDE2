from django.urls import path
from . import views

app_name = 'inscripcion'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard_promotor, name='dashboard_promotor'),
    
    # Equipos
    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('equipos/crear/', views.crear_equipo, name='crear_equipo'),
    path('equipos/<int:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),
    path('equipos/<int:equipo_id>/editar/', views.editar_equipo, name='editar_equipo'),
    
    # Jugadores
    path('jugadores/', views.lista_jugadores, name='lista_jugadores'),
    path('equipos/<int:equipo_id>/jugadores/crear/', views.crear_jugador, name='crear_jugador'),
    path('jugadores/<int:jugador_id>/editar/', views.editar_jugador, name='editar_jugador'),
    path('jugadores/<int:jugador_id>/eliminar/', views.eliminar_jugador, name='eliminar_jugador'),
    
    # Pagos
    path('equipos/<int:equipo_id>/pago/', views.pago_inscripcion, name='pago_inscripcion'),
    path('pagos/<int:pago_id>/confirmacion/', views.confirmacion_pago, name='confirmacion_pago'),
    path('pagos/', views.lista_pagos, name='lista_pagos'),

]