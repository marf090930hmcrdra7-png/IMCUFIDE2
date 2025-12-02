from django.shortcuts import render


# ESTE APARTADO DE FUNCIONES ES PARA CREAR, ELIMINAR MOSTRAR Y ACTUALIZAR LAS ESTADISTICAS 
from django.shortcuts import render, redirect, get_object_or_404
from .models import estadisticas, equipo

#CREAR ESTADISTICAS

def crear_estadistica(request):
    equipos = equipo.objects.all()

    if request.method == "POST":
        id_equipo = request.POST["equipo"]
        jj = request.POST["jj"]
        jg = request.POST["jg"]
        jp = request.POST["jp"]
        puntos = request.POST["puntos"]
        gaf = request.POST["gaf"]
        gc = request.POST["gc"]
        dif = request.POST["dif"]
        amon = request.POST["amon"]

        estadisticas.objects.create(
            equipo_id=id_equipo,
            jj=jj,
            jg=jg,
            jp=jp,
            puntos=puntos,
            gaf=gaf,
            gc=gc,
            dif=dif,
            amonestaciones=amon,
        )

        return redirect("tabla_posiciones")

    return render(request, "crear_estadistica.html", {"equipos": equipos})


#EDUTAR ESTADISTICAS
def editar_estadistica(request, id):
    dato = get_object_or_404(estadisticas, id=id)
    equipos = equipo.objects.all()

    if request.method == "POST":
        dato.jj = request.POST["jj"]
        dato.jg = request.POST["jg"]
        dato.jp = request.POST["jp"]
        dato.puntos = request.POST["puntos"]
        dato.gaf = request.POST["gaf"]
        dato.gc = request.POST["gc"]
        dato.dif = request.POST["dif"]
        dato.amonestaciones = request.POST["amon"]
        dato.save()

        return redirect("tabla_posiciones")

    return render(request, "editar_estadistica.html", {"dato": dato, "equipos": equipos})

#eLIMINAR ESTADISTICAS
def eliminar_estadistica(request, id):
    dato = get_object_or_404(estadisticas, id=id)
    dato.delete()
    return redirect("tabla_posiciones")


# MOSTRAR ESTADISTICAS
def tabla_posiciones(request):
    tabla = estadisticas.objects.select_related("equipo").order_by("-puntos", "-dif")
    return render(request, "tabla_posiciones.html", {"tabla": tabla})




from django.shortcuts import render
from django_tables2 import SingleTableView

def inicio(request):
    return render(request,'Inicio.html')

from .models import estadisticas
from .tables import estadisticas2

class PersonListView(SingleTableView):
    model = estadisticas
    table_class = estadisticas2
    template_name = 'Tabla.html'