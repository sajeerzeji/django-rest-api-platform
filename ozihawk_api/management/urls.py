from django.urls import path, include
from .views import ManagementHelloWorld

urlpatterns = [
    path('hello/', ManagementHelloWorld.as_view()),
]