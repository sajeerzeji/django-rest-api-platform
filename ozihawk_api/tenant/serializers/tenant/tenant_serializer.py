from rest_framework import serializers


class TenantSerializer(serializers.Serializer):
    tenant_name = serializers.CharField()