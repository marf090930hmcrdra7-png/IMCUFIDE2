from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Equipo, Jugador, PagoInscripcion, Categoria
from .forms import (EquipoForm, JugadorForm, PagoInscripcionForm, 
                    BuscarEquipoForm, BuscarJugadorForm)

def dashboard_promotor(request):
    equipos = Equipo.objects.all().annotate(
        num_jugadores=Count('jugadores')
    )
    
    context = {
        'equipos': equipos,
        'total_equipos': equipos.count(),
        'equipos_activos': equipos.filter(estado='activo').count(),
        'equipos_pendientes': equipos.filter(estado='pendiente').count(),
    }
    return render(request, 'inscripcion/dashboard_promotor.html', context)


def lista_equipos(request):
    equipos = Equipo.objects.all().select_related('categoria', 'promotor').annotate(
        num_jugadores=Count('jugadores')
    )
    
    form = BuscarEquipoForm(request.GET)
    
    if form.is_valid():
        buscar = form.cleaned_data.get('buscar')
        categoria = form.cleaned_data.get('categoria')
        estado = form.cleaned_data.get('estado')
        
        if buscar:
            equipos = equipos.filter(
                Q(nombre__icontains=buscar) | 
                Q(nombre_promotor__icontains=buscar)
            )
        
        if categoria:
            equipos = equipos.filter(categoria=categoria)
        
        if estado:
            equipos = equipos.filter(estado=estado)
    
    context = {
        'equipos': equipos,
        'form': form,
    }
    return render(request, 'inscripcion/lista_equipos.html', context)


def detalle_equipo(request, equipo_id):
    equipo = get_object_or_404(
        Equipo.objects.select_related('categoria', 'promotor').annotate(
            num_jugadores=Count('jugadores')
        ),
        id=equipo_id
    )
    
    jugadores = equipo.jugadores.filter(activo=True).order_by('numero_camiseta')
    pagos = equipo.pagos.all().order_by('-fecha_pago')
    
    context = {
        'equipo': equipo,
        'jugadores': jugadores,
        'pagos': pagos,
    }
    return render(request, 'inscripcion/detalle_equipo.html', context)


def crear_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST, request.FILES)
        if form.is_valid():
            equipo = form.save(commit=False)

            if request.user.is_authenticated:
                equipo.promotor = request.user
            else:
                equipo.promotor = None

            equipo.save()

            messages.success(request, f'Equipo "{equipo.nombre}" creado exitosamente.')
            return redirect('inscripcion:pago_inscripcion', equipo_id=equipo.id)
    else:
        form = EquipoForm()
    
    context = {
        'form': form,
        'titulo': 'Registrar Nuevo Equipo'
    }
    return render(request, 'inscripcion/form_equipo.html', context)


def editar_equipo(request, equipo_id):
    if request.user.is_superuser:
        equipo = get_object_or_404(Equipo, id=equipo_id, promotor=request.user)
    else:
        equipo = get_object_or_404(Equipo, id=equipo_id)
 
    if request.method == 'POST':
        form = EquipoForm(request.POST, request.FILES, instance=equipo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Equipo "{equipo.nombre}" actualizado exitosamente.')
            return redirect('inscripcion:detalle_equipo', equipo_id=equipo.id)
    else:
        form = EquipoForm(instance=equipo)
    
    context = {
        'form': form,
        'equipo': equipo,
        'titulo': f'Editar Equipo: {equipo.nombre}'
    }
    return render(request, 'inscripcion/form_equipo.html', context)


def lista_jugadores(request):
    jugadores = Jugador.objects.filter(activo=True).select_related('equipo', 'equipo__categoria')
    
    form = BuscarJugadorForm(request.GET)
    
    if form.is_valid():
        buscar = form.cleaned_data.get('buscar')
        posicion = form.cleaned_data.get('posicion')
        
        if buscar:
            jugadores = jugadores.filter(
                Q(nombre__icontains=buscar) | 
                Q(apellido__icontains=buscar) |
                Q(equipo__nombre__icontains=buscar)
            )
        
        if posicion:
            jugadores = jugadores.filter(posicion=posicion)
    
    context = {
        'jugadores': jugadores,
        'form': form,
    }
    return render(request, 'inscripcion/lista_jugadores.html', context)


def crear_jugador(request, equipo_id):
    if request.user.is_superuser:
        equipo = get_object_or_404(Equipo, id=equipo_id, promotor=request.user)
    else:
        equipo = get_object_or_404(Equipo, id=equipo_id)
    
    if request.method == 'POST':
        form = JugadorForm(request.POST, request.FILES, equipo=equipo)
        if form.is_valid():
            jugador = form.save(commit=False)
            jugador.equipo = equipo
            jugador.save()
            messages.success(request, f'Jugador "{jugador.nombre} {jugador.apellido}" agregado exitosamente.')
            return redirect('inscripcion:detalle_equipo', equipo_id=equipo.id)
    else:
        form = JugadorForm(equipo=equipo)
    
    context = {
        'form': form,
        'equipo': equipo,
        'titulo': f'Agregar Jugador a {equipo.nombre}'
    }
    return render(request, 'inscripcion/form_jugador.html', context)


def editar_jugador(request, jugador_id):
    if request.user.is_superuser:
        jugador = get_object_or_404(Jugador, id=jugador_id, equipo__promotor=request.user)
    else:
        jugador = get_object_or_404(Jugador, id=jugador_id)

        equipo = jugador.equipo
    
    if request.method == 'POST':
        form = JugadorForm(request.POST, request.FILES, instance=jugador, equipo=equipo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Jugador "{jugador.nombre} {jugador.apellido}" actualizado exitosamente.')
            return redirect('inscripcion:detalle_equipo', equipo_id=equipo.id)
    else:
        form = JugadorForm(instance=jugador, equipo=equipo)
    
    context = {
        'form': form,
        'jugador': jugador,
        'equipo': equipo,
        'titulo': f'Editar Jugador: {jugador.nombre} {jugador.apellido}'
    }
    return render(request, 'inscripcion/form_jugador.html', context)


def eliminar_jugador(request, jugador_id):
    if request.user.is_authenticated:
        jugador = get_object_or_404(Jugador, id=jugador_id, equipo__promotor=request.user)
    else:
        jugador = get_object_or_404(Jugador, id=jugador_id)

    equipo = jugador.equipo
    
    if request.method == 'POST':
        jugador.activo = False
        jugador.save()
        messages.success(request, f'Jugador "{jugador.nombre} {jugador.apellido}" eliminado del equipo.')
        return redirect('inscripcion:detalle_equipo', equipo_id=equipo.id)
    
    context = {
        'jugador': jugador,
        'equipo': equipo,
    }
    return render(request, 'inscripcion/confirmar_eliminar_jugador.html', context)


def pago_inscripcion(request, equipo_id):
    if request.user.is_authenticated:
        equipo = get_object_or_404(Equipo, id=equipo_id, promotor=request.user)
    else:
        equipo = get_object_or_404(Equipo, id=equipo_id)

    
    if request.method == 'POST':
        form = PagoInscripcionForm(request.POST, request.FILES)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.equipo = equipo
            pago.estado = 'verificando'
            pago.save()
            
            equipo.estado = 'pagado'
            equipo.fecha_pago = timezone.now()
            equipo.save()
            
            messages.success(request, 'Pago registrado exitosamente. Será verificado por el administrador.')
            return redirect('inscripcion:confirmacion_pago', pago_id=pago.id)
    else:
        form = PagoInscripcionForm(initial={'monto': equipo.monto_inscripcion})
    
    context = {
        'form': form,
        'equipo': equipo,
    }
    return render(request, 'inscripcion/pago_inscripcion.html', context)


def confirmacion_pago(request, pago_id):
    if request.user.is_superuser:
        pago = get_object_or_404(PagoInscripcion, id=pago_id, equipo__promotor=request.user)
    else:
        pago = get_object_or_404(PagoInscripcion, id=pago_id)
    
    context = {
        'pago': pago,
        'equipo': pago.equipo,
    }
    return render(request, 'inscripcion/confirmacion_pago.html', context)


def lista_pagos(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('inscripcion:dashboard_promotor')
    
    pagos = PagoInscripcion.objects.all().select_related('equipo', 'verificado_por').order_by('-fecha_pago')
    
    context = {
        'pagos': pagos,
    }
    return render(request, 'inscripcion/lista_pagos.html', context)