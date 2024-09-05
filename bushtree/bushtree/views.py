from rest_framework import (status, viewsets)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from bushtree.serializers import *
from bushtree.mixin import *

class FLowerApiView(APIView):
    
    def get(self, request):
        flowers = Flowers.objects.all()
        return Response({"data": flowers}, status=status.HTTP_200_OK)