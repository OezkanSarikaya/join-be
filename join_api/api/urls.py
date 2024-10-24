from django.contrib import admin
from django.urls import path, include
from .views import ContactViewSet, TaskViewSet
from rest_framework import routers
from rest_framework.routers import SimpleRouter

# router = routers.SimpleRouter()
router = SimpleRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
]