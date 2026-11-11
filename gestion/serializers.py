from rest_framework import serializers
from .models import Plan, Membresia, ClaseGrupal, Reserva

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class MembresiaSerializer(serializers.ModelSerializer):
    # Mostramos el nombre del usuario y plan en vez de solo su ID numérico
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')
    plan_nombre = serializers.ReadOnlyField(source='plan.nombre')

    class Meta:
        model = Membresia
        fields = '__all__'

class ClaseGrupalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaseGrupal
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')
    clase_nombre = serializers.ReadOnlyField(source='clase.nombre')

    class Meta:
        model = Reserva
        fields = '__all__'