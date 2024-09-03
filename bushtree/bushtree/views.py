from rest_framework import (status, viewsets)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action
from bushtree.serializers import *
from bushtree.models import *
from bushtree.mixin import *
import array

class FLowerApiView(APIView):
    
    def get(self, request):
        flowers = Flowers.objects.all()
        return Response({"data": flowers}, status=status.HTTP_200_OK)

class SeccionApiViewSet(viewsets.ModelViewSet):
    
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer

    def list(self, request, *args, **kwargs):
        seccions = self.get_queryset()
        serializers = self.get_serializer(seccions)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"])
    def create_seccion(self, request):
        serializers = self.get_serializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.error, status=status.HTTP_403_FORBIDDEN)

    
        