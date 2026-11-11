from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, ClaseGrupalViewSet, MembresiaViewSet, ReservaViewSet, dashboard_view

router = DefaultRouter()
router.register(r'planes', PlanViewSet)
router.register(r'clases', ClaseGrupalViewSet)
router.register(r'membresias', MembresiaViewSet)
router.register(r'reservas', ReservaViewSet)

urlpatterns = [
    path('', include(router.urls)), # Esta es la API (ej: /api/membresias/)
    path('dashboard/', dashboard_view, name='dashboard'), # Esta es la interfaz web (ej: /api/dashboard/)
]