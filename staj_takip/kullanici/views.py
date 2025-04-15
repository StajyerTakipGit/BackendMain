from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenAlSerializer

class GirisAPIView(TokenObtainPairView):
    serializer_class = TokenAlSerializer
