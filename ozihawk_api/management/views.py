from tenant.serializers.serializers import UserSerializer
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework import generics, permissions
from rest_framework.generics import RetrieveAPIView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope


# Create your views here.

class ManagementHelloWorld(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer
