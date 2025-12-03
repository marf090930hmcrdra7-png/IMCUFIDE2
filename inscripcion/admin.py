from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Categoria, Equipo, Jugador, PagoInscripcion


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'edad_minima', 'edad_maxima', 'descripcion']
    list_filter = ['edad_minima', 'edad_maxima']
    search_fields = ['nombre', 'descripcion']


class JugadorInline(admin.TabularInline):
    model = Jugador
    extra = 0
    fields = ['nombre', 'apellido', 'numero_camiseta', 'posicion', 'edad', 'activo']
    readonly_fields = ['fecha_registro']


class PagoInline(admin.TabularInline):
    model = PagoInscripcion
    extra = 0
    fields = ['monto', 'metodo_pago', 'estado', 'fecha_pago']
    readonly_fields = ['fecha_pago']


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'promotor', 'estado', 'total_jugadores_admin', 'fecha_inscripcion']
    list_filter = ['estado', 'categoria', 'fecha_inscripcion']
    search_fields = ['nombre', 'nombre_promotor', 'promotor__username', 'promotor__email']
    readonly_fields = ['fecha_inscripcion', 'fecha_pago', 'total_jugadores_admin']
    inlines = [JugadorInline, PagoInline]
    
    fieldsets = (
        ('Información del Equipo', {
            'fields': ('nombre', 'categoria', 'logo', 'promotor')
        }),
        ('Información del Promotor', {
            'fields': ('nombre_promotor', 'telefono_promotor', 'email_promotor')
        }),
        ('Estado y Control', {
            'fields': ('estado', 'fecha_inscripcion', 'fecha_pago', 'total_jugadores_admin')
        }),
        ('Información de Pago', {
            'fields': ('monto_inscripcion', 'comprobante_pago')
        }),
    )
    
    def total_jugadores_admin(self, obj):
        return obj.jugadores.filter(activo=True).count()
    total_jugadores_admin.short_description = 'Jugadores Activos'
    
    actions = ['aprobar_equipos', 'desactivar_equipos']
    
    def aprobar_equipos(self, request, queryset):
        queryset.update(estado='activo')
        self.message_user(request, f'{queryset.count()} equipo(s) aprobado(s).')
    aprobar_equipos.short_description = 'Aprobar equipos seleccionados'
    
    def desactivar_equipos(self, request, queryset):
        queryset.update(estado='inactivo')
        self.message_user(request, f'{queryset.count()} equipo(s) desactivado(s).')
    desactivar_equipos.short_description = 'Desactivar equipos seleccionados'


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'equipo', 'numero_camiseta', 'posicion', 'edad', 'activo']
    list_filter = ['posicion', 'activo', 'equipo__categoria', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'equipo__nombre', 'documento_identidad']
    readonly_fields = ['fecha_registro']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'fecha_nacimiento', 'edad', 'documento_identidad', 'foto')
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'email', 'direccion')
        }),
        ('Información Deportiva', {
            'fields': ('equipo', 'posicion', 'numero_camiseta')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_registro')
        }),
    )
    
    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    nombre_completo.short_description = 'Nombre Completo'
    
    actions = ['activar_jugadores', 'desactivar_jugadores']
    
    def activar_jugadores(self, request, queryset):
        queryset.update(activo=True)
        self.message_user(request, f'{queryset.count()} jugador(es) activado(s).')
    activar_jugadores.short_description = 'Activar jugadores seleccionados'
    
    def desactivar_jugadores(self, request, queryset):
        queryset.update(activo=False)
        self.message_user(request, f'{queryset.count()} jugador(es) desactivado(s).')
    desactivar_jugadores.short_description = 'Desactivar jugadores seleccionados'


@admin.register(PagoInscripcion)
class PagoInscripcionAdmin(admin.ModelAdmin):
    list_display = ['equipo', 'monto', 'metodo_pago', 'estado_badge', 'fecha_pago', 'verificado_por']
    list_filter = ['estado', 'metodo_pago', 'fecha_pago']
    search_fields = ['equipo__nombre', 'referencia']
    readonly_fields = ['fecha_pago', 'fecha_verificacion', 'comprobante_preview']
    
    fieldsets = (
        ('Información del Pago', {
            'fields': ('equipo', 'monto', 'metodo_pago', 'referencia')
        }),
        ('Comprobante', {
            'fields': ('comprobante', 'comprobante_preview')
        }),
        ('Estado y Verificación', {
            'fields': ('estado', 'fecha_pago', 'fecha_verificacion', 'verificado_por', 'notas')
        }),
    )
    
    def estado_badge(self, obj):
        colors = {
            'pendiente': '#ffc107',
            'verificando': '#17a2b8',
            'aprobado': '#28a745',
            'rechazado': '#dc3545',
        }
        color = colors.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def comprobante_preview(self, obj):
        if obj.comprobante:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px;" />',
                obj.comprobante.url
            )
        return "Sin comprobante"
    comprobante_preview.short_description = 'Vista Previa'
    
    actions = ['aprobar_pagos', 'rechazar_pagos']
    
    def aprobar_pagos(self, request, queryset):
        for pago in queryset:
            pago.estado = 'aprobado'
            pago.verificado_por = request.user
            pago.fecha_verificacion = timezone.now()
            pago.save()
            
            # Actualizar estado del equipo
            pago.equipo.estado = 'activo'
            pago.equipo.save()
        
        self.message_user(request, f'{queryset.count()} pago(s) aprobado(s).')
    aprobar_pagos.short_description = 'Aprobar pagos seleccionados'
    
    def rechazar_pagos(self, request, queryset):
        for pago in queryset:
            pago.estado = 'rechazado'
            pago.verificado_por = request.user
            pago.fecha_verificacion = timezone.now()
            pago.save()
        
        self.message_user(request, f'{queryset.count()} pago(s) rechazado(s).')
    rechazar_pagos.short_description = 'Rechazar pagos seleccionados'


# Personalización del admin site
admin.site.site_header = "Sistema Deportivo - Administración"
admin.site.site_title = "Admin Sistema Deportivo"
admin.site.index_title = "Panel de Control"