import random
from .models import Plan, Membresia, ClaseGrupal, Reserva
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .serializers import PlanSerializer, MembresiaSerializer, ClaseGrupalSerializer, ReservaSerializer



class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class ClaseGrupalViewSet(viewsets.ModelViewSet):
    queryset = ClaseGrupal.objects.all()
    serializer_class = ClaseGrupalSerializer

class MembresiaViewSet(viewsets.ModelViewSet):
    queryset = Membresia.objects.all()
    serializer_class = MembresiaSerializer

    @action(detail=False, methods=['post'])
    def validar_acceso(self, request):
        codigo_qr = request.data.get('codigo_qr')
        if not codigo_qr:
            return Response({'error': 'Código QR no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            membresia = Membresia.objects.get(codigo_qr=codigo_qr)
            hoy = timezone.now().date()
            
            if membresia.estado != 'Activa':
                return Response({'acceso': 'Denegado', 'motivo': f'Membresía {membresia.estado}'}, status=status.HTTP_403_FORBIDDEN)
            
            if hoy > membresia.fecha_fin:
                membresia.estado = 'Vencida'
                membresia.save()
                return Response({'acceso': 'Denegado', 'motivo': 'Membresía Vencida'}, status=status.HTTP_403_FORBIDDEN)
                
            return Response({'acceso': 'Permitido', 'usuario': membresia.usuario.username})
            
        except Membresia.DoesNotExist:
            return Response({'acceso': 'Denegado', 'motivo': 'QR Inválido'}, status=status.HTTP_404_NOT_FOUND)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def create(self, request, *args, **kwargs):
        clase_id = request.data.get('clase')
        usuario_id = request.data.get('usuario')
        
        try:
            clase = ClaseGrupal.objects.get(id=clase_id)
        except ClaseGrupal.DoesNotExist:
            return Response({'error': 'La clase no existe'}, status=status.HTTP_404_NOT_FOUND)

        if clase.cupos_disponibles > 0:
            clase.cupos_disponibles -= 1
            clase.save()
            en_lista_espera = False
            mensaje = "Reserva confirmada exitosamente."
        else:
            en_lista_espera = True
            mensaje = "Clase llena. Has sido añadido a la lista de espera automáticamente."

        reserva = Reserva.objects.create(
            usuario_id=usuario_id,
            clase=clase,
            en_lista_espera=en_lista_espera
        )
        
        serializer = self.get_serializer(reserva)
        return Response({'mensaje': mensaje, 'reserva': serializer.data}, status=status.HTTP_201_CREATED)

def custom_login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            # Redirección obligatoria al Dashboard para TODO tipo de usuario
            return redirect('/api/dashboard/')
        else:
            return render(request, 'login.html', {'form': {'errors': True}})
            
    return render(request, 'login.html')

def registro_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        # Validar que el usuario no exista
        if User.objects.filter(username=u).exists():
            return render(request, 'registro.html', {'error': 'Este usuario ya está registrado.'})
            
        # Crear el usuario en PostgreSQL de forma segura
        user = User.objects.create_user(username=u, password=p)
        login(request, user) # Iniciar sesión automáticamente
        return redirect('/api/dashboard/')
        
    return render(request, 'registro.html')

def iniciar_pago_webpay(request, precio):
    try:
        opciones = WebpayOptions(
            "597055555532", 
            "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C", 
            IntegrationType.TEST
        )
        tx = Transaction(opciones)
        
        id_unico = str(random.randint(1000000, 9999999))
        
        # Transbank devuelve un diccionario en esta versión
        respuesta = tx.create(
            buy_order=f"ORDEN-{id_unico}",
            session_id=f"SESION-{id_unico}",
            amount=precio,
            return_url="http://127.0.0.1:8000/api/dashboard/"
        )
        
        # Extraemos usando la sintaxis de diccionario ['clave']
        url_banco = respuesta['url']
        token_ws = respuesta['token']
        
        html = f"""
        <html><body style="background:#000; color:#fff; text-align:center; padding-top:20%; font-family:sans-serif;" onload="document.forms[0].submit()">
            <h2>Conectando de forma segura con Transbank...</h2>
            <form action="{url_banco}" method="POST">
                <input type="hidden" name="token_ws" value="{token_ws}">
            </form>
        </body></html>
        """
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"Error conectando a Webpay: {str(e)}", status=500)

@login_required(login_url='/login/')
def dashboard_view(request):
    return render(request, 'dashboard.html')

def home_view(request):
    return render(request, 'index.html')

def mi_error_404(request, exception):
    return render(request, '404.html', status=404)

def gimnasios_view(request):
    return render(request, 'gimnasios.html')

def tuespacio_view(request):
    return render(request, 'tuespacio.html')

def app_view(request):
    return render(request, 'app.html')