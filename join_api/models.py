from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Contact(models.Model):
    color = models.IntegerField(default=0)  # Farbe als Zahl, evtl. einheitlich verwenden
    email = models.EmailField()    # Verwende EmailField für E-Mails
    name = models.CharField(max_length=255)  # CharField für kurze Textinhalte
    # Hier evtl. PasswordField oder Hashing anwenden
    password = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)  # Phone-Feld mit begrenzter Länge
    is_user = models.BooleanField(default=False)  # True/False für Benutzerstatus
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="contact")

    def __str__(self):
        return self.name


class Task(models.Model):

    TODO = 1
    IN_PROGRESS = 2
    FEEDBACK = 3
    DONE = 4

    STATUS_CHOICES = [
        (TODO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (FEEDBACK, 'Await Feedback'),
        (DONE, 'Done'),
    ]

    TECHNICAL = 'Technical task'
    USER_STORY = 'User story'

    CATEGORY_CHOICES = [
        (TECHNICAL, 'Technical task'),
        (USER_STORY, 'User story')
    ]

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'urgent'

    PRIORITY_CHOICES = [
        (LOW, 'Low Priority'),
        (MEDIUM, 'Medium Priority'),
        (HIGH, 'High Priority'),
    ]

    # CharField für Kategorienamen
    categoryTask = models.CharField(max_length=255,
                                    choices=CATEGORY_CHOICES,  # Die Auswahlmöglichkeiten
                                    default=TECHNICAL  # Standardwert
                                    )
    descriptionTask = models.TextField(blank=True, null=True)  # TextField für längere Beschreibungen
    nameAssignedTask = models.ManyToManyField(
        Contact, related_name="tasks")  # ManyToManyField, ohne on_delete
    # CharField für kurze Texte zur Priorität
    priorityTask = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,  # Die Auswahlmöglichkeiten
        default=MEDIUM  # Standardwert
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,  # Die Auswahlmöglichkeiten
        default=TODO  # Standardwert
    )  # Status als Integer
    timeDeadlineTask = models.DateField()  # DateTimeField für Deadlines
    titleTask = models.CharField(max_length=255)  # CharField für kurze Titel

    def __str__(self):
        return self.titleTask


class SubTask(models.Model):
    # Verknüpfung zum übergeordneten Task
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="subTasks")
    subTaskName = models.CharField(max_length=255)  # Name des Subtasks
    # Status (True = abgeschlossen, False = offen)
    statusSubTask = models.BooleanField(default=False)

    def __str__(self):
        return self.subTaskName
