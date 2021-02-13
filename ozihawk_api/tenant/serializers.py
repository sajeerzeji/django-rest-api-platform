from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import Group, User

class ClientSerializer(serializers.Serializer):
     tenant_name = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")