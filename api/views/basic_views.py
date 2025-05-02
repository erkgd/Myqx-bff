from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import datetime
import logging
import sys

# Health Check view for server status
class HealthCheckView(APIView):
    """
    Endpoint para verificar el estado del servidor (health check).
    """
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        """
        Retorna un mensaje simple indicando que el servicio está funcionando.
        """
        data = {
            'status': 'ok',
            'message': 'BFF funcionando correctamente',
            'timestamp': datetime.datetime.now().isoformat(),
            'service': 'Myqx-BFF'
        }
        return Response(data, status=status.HTTP_200_OK)

# All user-related views moved to user_views.py
