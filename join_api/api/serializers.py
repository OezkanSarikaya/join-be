from rest_framework import serializers
from join_api.models import Contact, Task, SubTask

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id','subTaskName', 'statusSubTask']  # Die Felder des SubTasks

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)  # Erlaubt, nur bestimmte Felder zu wählen
        super(SubTaskSerializer, self).__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
class TaskSerializer(serializers.ModelSerializer):
    subTasks = SubTaskSerializer(many=True)  # Nested Serializer für Subtasks
    # Write-only für Kontakt-IDs
    nameAssignedTask = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        many=True,
        write_only=True
    )

    # Read-only für die Details der Kontakte
    nameAssignedTask_details = ContactSerializer(
        source="nameAssignedTask",  # Nimmt die Daten aus `nameAssignedTask`
        many=True,
        read_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'categoryTask', 'descriptionTask', 'nameAssignedTask',
            'nameAssignedTask_details', 'priorityTask', 'status',
            'timeDeadlineTask', 'titleTask', 'subTasks'
        ]

    def create(self, validated_data):
        # Extrahiere subtasks und die Kontakte
        subTasks_data = validated_data.pop('subTasks')
        contacts_data = validated_data.pop('nameAssignedTask')
        
        # Erstelle den Task ohne die Many-to-Many-Beziehung zu den Kontakten
        task = Task.objects.create(**validated_data)
        
        # Weise die Kontakte (nameAssignedTask) über die set()-Methode zu
        task.nameAssignedTask.set(contacts_data)
        
        # Erstelle die Subtasks und verknüpfe sie mit dem Task
        for subTasks_data in subTasks_data:
            SubTask.objects.create(task=task, **subTasks_data)
        
        return task
    
    def update(self, instance, validated_data):
        # Extrahiere die Subtask-Daten
        subtasks_data = validated_data.pop('subTasks')
        contacts_data = validated_data.pop('nameAssignedTask')

        # Update der Task-Felder
        instance.categoryTask = validated_data.get('categoryTask', instance.categoryTask)
        instance.descriptionTask = validated_data.get('descriptionTask', instance.descriptionTask)
        instance.priorityTask = validated_data.get('priorityTask', instance.priorityTask)
        instance.status = validated_data.get('status', instance.status)
        instance.timeDeadlineTask = validated_data.get('timeDeadlineTask', instance.timeDeadlineTask)
        instance.titleTask = validated_data.get('titleTask', instance.titleTask)
        instance.save()

        # Kontakte aktualisieren
        instance.nameAssignedTask.set(contacts_data)

        # Subtasks aktualisieren
        existing_subtask_ids = [subtask.id for subtask in instance.subTasks.all()]
        new_subtask_ids = [item.get('id') for item in subtasks_data if 'id' in item]

        # Entferne Subtasks, die nicht mehr vorhanden sind
        for subtask_id in existing_subtask_ids:
            if subtask_id not in new_subtask_ids:
                SubTask.objects.filter(id=subtask_id).delete()

        # Subtasks aktualisieren oder erstellen
        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id', None)
            if subtask_id and subtask_id in existing_subtask_ids:
                # Wenn der Subtask existiert, aktualisieren
                subtask = SubTask.objects.get(id=subtask_id, task=instance)
                subtask.subTaskName = subtask_data.get('subTaskName', subtask.subTaskName)
                subtask.statusSubTask = subtask_data.get('statusSubTask', subtask.statusSubTask)
                subtask.save()
            else:
                # Neuen Subtask erstellen
                SubTask.objects.create(task=instance, **subtask_data)

        return instance
    
    

