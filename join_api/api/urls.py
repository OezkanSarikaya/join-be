from django.contrib import admin
from django.urls import path, include
from .views import ContactViewSet, TaskViewSet, SubTaskViewSet
from rest_framework import routers
from rest_framework.routers import SimpleRouter

# router = routers.SimpleRouter()
router = SimpleRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubTaskViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
]