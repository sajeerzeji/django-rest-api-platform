"""ozihawk_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from users.views import GroupList
# from users.views import UserDetails, UserList
from ozihawk_api.views import ApiEndpoint, CustomRevokeTokenView, CustomTokenView
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
import oauth2_provider.views as oauth2_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/applications/register', oauth2_views.ApplicationRegistration.as_view(), name="application_registeration"),
    path('o/authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('o/token/', CustomTokenView.as_view(), name="token"),
    # path('o/revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
    path('o/revoke-token/', CustomRevokeTokenView.as_view(), name="revoke-token"),
    path('tenant/', include('tenant.urls')),
    path('management/', include('management.urls')),
    # path('users/', UserList.as_view()),
    # path('users/<pk>/', UserDetails.as_view()),
    # path('groups/', GroupList.as_view()),
]
