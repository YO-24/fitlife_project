from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    imagen_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planes"

    def __str__(self):
        return self.nombre

class Membresia(models.Model):
    ESTADOS_MEMBRESIA = [
        ('Activa', 'Activa'),
        ('Vencida', 'Vencida'),
        ('Congelada', 'Congelada'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_MEMBRESIA, default='Activa')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    codigo_qr = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = "Membresía"
        verbose_name_plural = "Membresías"

    def __str__(self):
        return f"{self.usuario.username} - {self.plan.nombre} ({self.estado})"

class ClaseGrupal(models.Model):
    nombre = models.CharField(max_length=100)
    profesor = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField()
    cupo_maximo = models.PositiveIntegerField()
    cupos_disponibles = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Clase Grupal"
        verbose_name_plural = "Clases Grupales"

    def __str__(self):
        return f"{self.nombre} - {self.fecha_hora.strftime('%d/%m %H:%M')}"

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    clase = models.ForeignKey(ClaseGrupal, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    # Este campo es vital para el requerimiento de "lista de espera automatizada"
    en_lista_espera = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        unique_together = ('usuario', 'clase') # Evita que alguien reserve dos veces la misma clase

    def __str__(self):
        estado = "En espera" if self.en_lista_espera else "Confirmada"
        return f"{self.usuario.username} -> {self.clase.nombre} ({estado})"