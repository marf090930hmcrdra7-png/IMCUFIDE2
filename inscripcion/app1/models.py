from django.db import models


class deporte(models.Model):
    iddeporte = models.AutoField(primary_key=True)
    nombredeporte = models.CharField(max_length=20)
    def __str__(self):
        return self.nombredeporte
    
class categoria(models.Model):
    nombrecategoria = models.CharField(max_length=20)
    dep = models.ForeignKey(deporte, on_delete=models.CASCADE)

class rama(models.Model):
    nombrerama = models.CharField(max_length=20)
    pertenencia = models.ForeignKey(categoria,on_delete=models.CASCADE)

class equipo(models.Model):
    nombreequipo = models.CharField(max_length=30)
    pertenenciarama = models.ForeignKey(rama,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombreequipo
    
class jugador(models.Model):
    nombrejugador = models.CharField(max_length=50)
    apellidopaterno = models.CharField(max_length=50)
    pertenencia = models.ForeignKey(equipo,on_delete=models.CASCADE,default=0)

class estadisticas(models.Model):
    equipo = models.OneToOneField(equipo,on_delete=models.CASCADE)
    jj = models.IntegerField()
    jg = models.IntegerField()
    jp = models.IntegerField()
    puntos = models.IntegerField()
    gaf = models.IntegerField()
    gc = models.IntegerField()
    dif = models.IntegerField()
    amonestaciones = models.IntegerField()
    def __str__(self):
        return self.equipos.nombreequipo

class partidos(models.Model):
    nombrepartido= models.CharField(max_length=50)
    equipopartido = models.ForeignKey(equipo,on_delete=models.CASCADE)

