from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from join_api.models import Contact, Task, SubTask
from .serializers import ContactSerializer, TaskSerializer, SubTaskSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrAdmin
# from user_auth_app.models import UserProfile

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsOwnerOrAdmin]

class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['patch'], url_path='update_status')
    def update_status(self, request, pk=None):
        task = self.get_object()  # Der spezifische Task
        # Status aus der Anfrage entnehmen
        new_status = request.data.get("status")

        if new_status is None:
            return Response({"error": "Status field is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Task-Status aktualisieren
        task.status = new_status
        task.save()

        # Aktualisierten Task zurückgeben
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='subtasks')
    def list_subtasks(self, request, pk=None):
        try:
            task = self.get_object()  # Den entsprechenden Task abrufen
            subtasks = task.subTasks.all()  # Alle Subtasks des Tasks abrufen
            serializer = SubTaskSerializer(
                subtasks, many=True)  # Subtasks serialisieren
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

     # Custom Action to retrieve a single subtask
    @action(detail=True, methods=['get'], url_path='subtasks/(?P<subtask_id>[^/.]+)')
    def retrieve_subtask(self, request, pk=None, subtask_id=None):
        # Get the specific task
        task = self.get_object()

        # Get the specific subtask within the task
        subtask = get_object_or_404(SubTask, pk=subtask_id, task=task)

        # Serialize the subtask and return the response
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Custom Action, um nur `statusSubTask` eines Subtasks zu aktualisieren (PATCH)
    @action(detail=True, methods=['patch'], url_path='update_subtask_status/(?P<subtask_id>[^/.]+)')
    def update_subtask_status(self, request, pk=None, subtask_id=None):
        try:
            subtask = SubTask.objects.get(pk=subtask_id, task_id=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

        # Nur `statusSubTask` wird aus `request.data` extrahiert und zum Aktualisieren verwendet
        status_serializer = SubTaskSerializer(subtask, data=request.data, fields=[
                                              'statusSubTask'], partial=True)

        if status_serializer.is_valid():
            status_serializer.save()
            return Response(status_serializer.data, status=status.HTTP_200_OK)
        return Response(status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     # Custom Action, um einen Subtask zu aktualisieren (PUT)

    @action(detail=True, methods=['put', 'patch'], url_path='edit_subtask/(?P<subtask_id>[^/.]+)')
    def edit_subtask(self, request, pk=None, subtask_id=None):
        try:
            subtask = SubTask.objects.get(pk=subtask_id, task_id=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

        subtask_serializer = SubTaskSerializer(
            subtask, data=request.data, partial=True)

        if subtask_serializer.is_valid():
            subtask_serializer.save()
            return Response(subtask_serializer.data, status=status.HTTP_200_OK)
        return Response(subtask_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
