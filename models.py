from django.db import models

class Convocatoria(models.Model):
    # Primary Key
    ID_convocatoria = models.AutoField(primary_key=True)
    
    # Nombre hasta arriba (después del ID)
    nombre = models.CharField(max_length=200)
    
    # Resto de campos en orden
    deporte = models.CharField(max_length=100)
    descripción = models.TextField(blank=True, null=True)
    
    CATEGORIAS = [
        ('Femenil', 'Femenil'),
        ('Varonil', 'Varonil'),
        ('Mixto', 'Mixto'),
    ]
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    
    ESTADOS = [
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada'),
        ('Finalizada', 'Finalizada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Abierta')
    
    fecha_inicio = models.DateField()
    fecha_limite = models.DateField()
    costos = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bases = models.TextField(blank=True, null=True)
    rama = models.CharField(max_length=100, blank=True, null=True)
    cómite_organizador = models.CharField(max_length=200, blank=True, null=True)
    sistema_de_competencia = models.TextField(blank=True, null=True)
    inscripciones = models.TextField(blank=True, null=True)
    requisitos = models.TextField(blank=True, null=True)
    normatividad_aplicable = models.TextField(blank=True, null=True)
    premiación = models.TextField(blank=True, null=True)
    arbitraje = models.TextField(blank=True, null=True)
    junta_previa = models.TextField(blank=True, null=True)
    transitorios = models.TextField(blank=True, null=True)
    pie_de_pagina = models.TextField(blank=True, null=True)
    datos_de_contacto = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} – {self.deporte} ({self.categoria})"