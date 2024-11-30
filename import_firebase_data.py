import os
import django
import json

# Django-Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'join_backend.settings')  # Ersetze "your_project" durch den Projektnamen
django.setup()

from join_api.models import Contact, Task, SubTask
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Pfad zur JSON-Datei
firebase_json_path = 'firebase-data.json'


def create_guest_user():
    """
    Erstellt einen Guest User und gibt die User-Instanz zurück.
    """
    email = "guest@test.de"
    username = email
    password = "123456"  # Leeres Passwort
    
    # User erstellen
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    # Token generieren
    token, _ = Token.objects.get_or_create(user=user)
    print(f"Token für User {user.username}: {token.key}")  # Debug-Ausgabe des Tokens

    return user, token

def import_guest_contact():
    """
    Erstellt den Kontakt für den Guest User und verknüpft den User mit diesem Kontakt.
    """
    # Guest User erstellen
    user, token = create_guest_user()

    # Kontakt erstellen und mit dem User verknüpfen
    contact = Contact.objects.create(
        color=11,
        email="guest@test.de",
        name="Guest User",
        password="",  # Leeres Passwort
        phone="",
        is_user=True,
        user=user  # Verknüpfen mit dem User
    )

    # user_id (User-ID) wird automatisch in 'contact.user.id' gespeichert
    contact.user_id = user.id  # Optional, falls du die user_id explizit speichern möchtest (wird bereits durch `user` gemacht)
    contact.save()

    print(f"Guest Contact erstellt und User-ID {user.id} zugewiesen.")



def import_data():
    with open(firebase_json_path, 'r') as file:
        data = json.load(file)

    # Kontakte importieren
    contacts_data = data.get("contacts", {})
    contact_mapping = {}  # Zur Zuordnung von Firebase-ID zu Contact-Objekten
    for contact_id, contact_info in contacts_data.items():
        contact = Contact.objects.create(
            color=contact_info.get("color", 0),
            email=contact_info.get("email"),
            name=contact_info.get("name"),
            password=contact_info.get("password", ""),
            phone=contact_info.get("phone", ""),
            is_user=contact_info.get("user", False)
        )
        contact_mapping[contact_id] = contact

    print(f"{len(contact_mapping)} Kontakte erfolgreich importiert.")

    # Tasks und SubTasks importieren
    tasks_data = data.get("tasks", {})
    for task_id, task_info in tasks_data.items():
        # Task erstellen
        task = Task.objects.create(
            categoryTask=task_info.get("categoryTask"),
            descriptionTask=task_info.get("descriptionTask", ""),
            priorityTask=task_info.get("priorityTask", Task.MEDIUM),
            status=task_info.get("status", Task.TODO),
            timeDeadlineTask=task_info.get("timeDeadlineTask"),
            titleTask=task_info.get("titleTask")
        )

        # Many-to-Many-Kontakte zuweisen
        assigned_contacts = task_info.get("nameAssignedTask", [])
        for assigned_contact in assigned_contacts:
            if isinstance(assigned_contact, dict):
                email = assigned_contact.get("email")
                if email:
                    contact = Contact.objects.filter(email=email).first()
                    if contact:
                        task.nameAssignedTask.add(contact)

        # SubTasks erstellen
        sub_tasks = task_info.get("subTasks", [])
        for sub_task_info in sub_tasks:
            SubTask.objects.create(
                task=task,
                subTaskName=sub_task_info.get("subTaskName"),
                statusSubTask=sub_task_info.get("statusSubTask", False)
            )

    print(f"{len(tasks_data)} Tasks und zugehörige SubTasks erfolgreich importiert.")

if __name__ == "__main__":
    import_guest_contact()
    import_data()
