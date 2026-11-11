from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Plan, Membresia, ClaseGrupal, Reserva

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)

@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    # Columnas visuales optimizadas
    list_display = ('usuario', 'plan', 'estado', 'fecha_inicio', 'fecha_fin')
    # Filtros laterales exigidos
    list_filter = ('estado', 'plan')
    # Barra de búsqueda por usuario
    search_fields = ('usuario__username', 'codigo_qr')

@admin.register(ClaseGrupal)
class ClaseGrupalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor', 'fecha_hora', 'cupos_disponibles', 'cupo_maximo')
    list_filter = ('profesor', 'fecha_hora')
    search_fields = ('nombre', 'profesor')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'clase', 'fecha_reserva', 'en_lista_espera')
    list_filter = ('en_lista_espera', 'clase')
    search_fields = ('usuario__username', 'clase__nombre')

# Ocultar Grupos y Usuarios del panel
admin.site.unregister(Group)
# admin.site.unregister(User)
