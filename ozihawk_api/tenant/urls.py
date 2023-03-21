from django.urls import path, include

from tenant.views.tenant_view import TenantView

urlpatterns = [
    path('tenants/', TenantView.as_view({'get': 'get', 'post': 'create'}))
]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
#
# from tenant.views.tenant_view import TenantView
# from tenant.views.views import ClientViewSet
#
# router = DefaultRouter(trailing_slash=False)
# router.register(r'clients/', ClientViewSet, basename='clients')
# router.register(r'tenants/', TenantView, basename='tenants')
#
# urlpatterns = [
#     path('', include(router.urls))
# ]