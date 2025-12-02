from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Categoria(models.Model):
   nombre = models.CharField(max_length=50)
   edad_minima = models.IntegerField()
   edad_maxima = models.IntegerField()
   descripcion = models.TextField(blank=True)
  
   class Meta:
       verbose_name_plural = "CategorÃ­as"
  
   def __str__(self):
       return self.nombre




class Equipo(models.Model):
   ESTADO_CHOICES = [
       ('pendiente', 'Pendiente'),
       ('pagado', 'Pagado'),
       ('activo', 'Activo'),
       ('inactivo', 'Inactivo'),
   ]
  
   nombre = models.CharField(max_length=100, unique=True)
   categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
   promotor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipos',null=True, blank=True)


   nombre_promotor = models.CharField(max_length=100)
   telefono_promotor = models.CharField(max_length=15)
   email_promotor = models.EmailField()
  
   logo = models.ImageField(upload_to='equipos/logos/', blank=True, null=True)
  
   estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
   fecha_inscripcion = models.DateTimeField(auto_now_add=True)
   fecha_pago = models.DateTimeField(null=True, blank=True)
  
   monto_inscripcion = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   comprobante_pago = models.ImageField(upload_to='equipos/comprobantes/', blank=True, null=True)
  
   class Meta:
       ordering = ['-fecha_inscripcion']
  
   def __str__(self):
       return f"{self.nombre} - {self.categoria}"
  
   def total_jugadores(self):
       return self.jugadores.count()




class Jugador(models.Model):
   POSICION_CHOICES = [
       ('portero', 'Portero'),
       ('defensa', 'Defensa'),
       ('mediocampista', 'Mediocampista'),
       ('delantero', 'Delantero'),
   ]
  
   equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')
  
   nombre = models.CharField(max_length=100)
   apellido = models.CharField(max_length=100)
   fecha_nacimiento = models.DateField()
   edad = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)])
  
   telefono = models.CharField(max_length=15)
   email = models.EmailField(blank=True)
   direccion = models.TextField(blank=True)
  
   posicion = models.CharField(max_length=20, choices=POSICION_CHOICES)
   numero_camiseta = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
  
  
   foto = models.ImageField(upload_to='jugadores/fotos/', blank=True, null=True)
   documento_identidad = models.CharField(max_length=20)
  
   activo = models.BooleanField(default=True)
   fecha_registro = models.DateTimeField(auto_now_add=True)
  
   class Meta:
       ordering = ['numero_camiseta']
       unique_together = ['equipo', 'numero_camiseta']
  
   def __str__(self):
       return f"{self.nombre} {self.apellido} - #{self.numero_camiseta}"




class PagoInscripcion(models.Model):
   METODO_PAGO_CHOICES = [
       ('transferencia', 'Transferencia'),
       ('efectivo', 'Efectivo'),
       ('tarjeta', 'Tarjeta'),
   ]
  
   ESTADO_CHOICES = [
       ('pendiente', 'Pendiente'),
       ('verificando', 'En VerificaciÃ³n'),
       ('aprobado', 'Aprobado'),
       ('rechazado', 'Rechazado'),
   ]
  
   equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='pagos')
  
   monto = models.DecimalField(max_digits=10, decimal_places=2)
   metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
   referencia = models.CharField(max_length=100, blank=True)
  
   comprobante = models.ImageField(upload_to='pagos/comprobantes/')
  
   estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
  
   fecha_pago = models.DateTimeField(auto_now_add=True)
   fecha_verificacion = models.DateTimeField(null=True, blank=True)
  
   notas = models.TextField(blank=True)
   verificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos_verificados')
  
   def __str__(self):
       return f"Pago {self.equipo.nombre} - ${self.monto}"


