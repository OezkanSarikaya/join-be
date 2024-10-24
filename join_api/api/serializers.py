from rest_framework import serializers
from join_api.models import Contact, Task, SubTask

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'subTaskName', 'statusSubTask']  # Die Felder des SubTasks


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)  # Nested Serializer für Subtasks

    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['id', 'categoryTask', 'descriptionTask', 'nameAssignedTask', 'priorityTask', 'status', 'timeDeadlineTask', 'titleTask', 'subtasks'] 