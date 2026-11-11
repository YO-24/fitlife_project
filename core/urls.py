from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from gestion.views import home_view, custom_login_view, mi_error_404, iniciar_pago_webpay, gimnasios_view, tuespacio_view, app_view, registro_view

urlpatterns = [
    path('', home_view, name='home'),
    path('gimnasios/', gimnasios_view, name='gimnasios'),
    path('tuespacio/', tuespacio_view, name='tuespacio'),
    path('app/', app_view, name='app'),
    path('admin/', admin.site.urls),
    path('api/', include('gestion.urls')),
    path('login/', custom_login_view, name='login'),
    path('registro/', registro_view, name='registro'), # <-- Nueva ruta de registro
    path('pago/<int:precio>/', iniciar_pago_webpay, name='webpay'),
]

handler404 = 'gestion.views.mi_error_404'