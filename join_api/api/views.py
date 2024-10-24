from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from join_api.models import Contact, Task, SubTask  
from .serializers import ContactSerializer, TaskSerializer, SubTaskSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset= Contact.objects.all()  
    serializer_class = ContactSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset= Task.objects.all()  
    serializer_class = TaskSerializer

    # Custom Action, um Subtasks zu erstellen
    @action(detail=True, methods=['post'])
    def add_subtask(self, request, pk=None):
        task = self.get_object()  # Der aktuelle Task
        subtask_data = request.data  # Daten vom Request
        subtask_serializer = SubTaskSerializer(data=subtask_data)  # SubTaskSerializer mit den Daten füttern

        if subtask_serializer.is_valid():
            subtask_serializer.save(task=task)  # Speichert den Subtask und verknüpft ihn mit dem Task
            return Response(subtask_serializer.data, status=status.HTTP_201_CREATED)
        return Response(subtask_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

     # Custom Action, um einen Subtask zu aktualisieren (PUT)
    @action(detail=True, methods=['put'], url_path='edit_subtask/(?P<subtask_id>[^/.]+)')
    def edit_subtask(self, request, pk=None, subtask_id=None):
        try:
            subtask = SubTask.objects.get(pk=subtask_id, task_id=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

        subtask_serializer = SubTaskSerializer(subtask, data=request.data, partial=True)

        if subtask_serializer.is_valid():
            subtask_serializer.save()
            return Response(subtask_serializer.data, status=status.HTTP_200_OK)
        return Response(subtask_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom Action, um einen Subtask zu löschen (DELETE)
    @action(detail=True, methods=['delete'], url_path='delete_subtask/(?P<subtask_id>[^/.]+)')
    def delete_subtask(self, request, pk=None, subtask_id=None):
        try:
            subtask = SubTask.objects.get(pk=subtask_id, task_id=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

        subtask.delete()
        return Response({'message': 'Subtask deleted'}, status=status.HTTP_204_NO_CONTENT)