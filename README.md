
# Join Backend API

Dies ist das Backend für das **Join**-Projekt, das mit Django und dem Django REST Framework entwickelt wurde. Es stellt Endpunkte für Kontakte, Aufgaben und Unteraufgaben (SubTasks) zur Verfügung.

## Voraussetzungen

1. **Python** 3.7+
2. **Django** (siehe `requirements.txt` für alle benötigten Bibliotheken)

## Installation

1. **Repository klonen**:
   ```bash
   git clone https://github.com/dein-benutzername/dein-repo.git
   cd dein-repo
   ```

2. **Virtuelle Umgebung erstellen und aktivieren**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # für Unix-Systeme
   venv\Scripts\activate  # für Windows
   ```

3. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

## Datenbank

Das Projekt verwendet eine SQLite-Datenbank, die bereits im Repository (`db.sqlite3`) vorhanden ist.

## Einstellungen

In der Datei `settings.py` müssen möglicherweise folgende Einstellungen angepasst werden:

```python
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:5500',
    'http://localhost:5500',
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5501",
    "http://localhost:5501",
]
```

Passen Sie die URLs an, falls das Frontend auf einer anderen Domain oder Port läuft.

## API Endpunkte

### 1. **Kontaktverwaltung**

- **Endpunkt:** `/api/contacts/`
- **Methoden:** `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

#### Beispiel:
- **GET /api/contacts/**:
  ```json
  [
    {
      "id": 1,
      "name": "Max Mustermann",
      "email": "max@example.com",
      "phone": "123456789",
      "user": true
    },
    ...
  ]
  ```

- **POST /api/contacts/**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "987654321",
    "user": true
  }
  ```

### 2. **Aufgabenverwaltung**

- **Endpunkt:** `/api/tasks/`
- **Methoden:** `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

#### Beispiel:
- **GET /api/tasks/**:
  ```json
  [
    {
      "id": 1,
      "titleTask": "API-Entwicklung",
      "categoryTask": "Technical task",
      "descriptionTask": "Implementiere die API",
      "priorityTask": "urgent",
      "status": 1,
      "timeDeadlineTask": "2024-12-31",
      "subTasks": [
        {
          "id": 1,
          "subTaskName": "API-Endpoints",
          "statusSubTask": false
        }
      ]
    }
  ]
  ```

- **PATCH /api/tasks/{task_id}/update_status/**: Aktualisiert den Status einer Aufgabe.
  - Beispiel-Request:
    ```json
    {
      "status": 2
    }
    ```

### 3. **Unteraufgaben (SubTasks)**

- **Endpunkt:** `/api/tasks/{task_id}/subtasks/`
  - **Methoden:** `GET` (Listet alle SubTasks einer Aufgabe auf)
  
- **Einzelner SubTask**: `/api/tasks/{task_id}/subtasks/{subtask_id}/`
  - **Methoden:** `GET` (Ruft einen bestimmten SubTask ab)
  
- **SubTask-Status aktualisieren**: `/api/tasks/{task_id}/update_subtask_status/{subtask_id}/`
  - **Methoden:** `PATCH`

#### Beispiel:
- **GET /api/tasks/1/subtasks/**:
  ```json
  [
    {
      "id": 1,
      "subTaskName": "API-Endpoints",
      "statusSubTask": false
    },
    ...
  ]
  ```

- **PATCH /api/tasks/1/update_subtask_status/1/**:
  - Beispiel-Request:
    ```json
    {
      "statusSubTask": true
    }
    ```

- **PATCH /api/tasks/1/edit_subtask/1/**:
  - Beispiel-Request zur vollständigen Aktualisierung eines SubTasks:
    ```json
    {
      "subTaskName": "Updated Subtask Name",
      "statusSubTask": true
    }
    ```

## Datenmodell

### 1. **Contact**
| Feld       | Typ         | Beschreibung                  |
|------------|-------------|-------------------------------|
| `id`       | Integer     | Primärschlüssel               |
| `name`     | CharField   | Name des Kontakts             |
| `email`    | EmailField  | Email-Adresse                 |
| `phone`    | CharField   | Telefonnummer                 |
| `user`     | Boolean     | Benutzerstatus (True/False)   |

### 2. **Task**
| Feld               | Typ            | Beschreibung                                     |
|--------------------|----------------|--------------------------------------------------|
| `id`               | Integer        | Primärschlüssel                                  |
| `titleTask`        | CharField      | Titel der Aufgabe                                |
| `categoryTask`     | ChoiceField    | Kategorie (z. B. Technical task, User story)     |
| `descriptionTask`  | TextField      | Beschreibung der Aufgabe                         |
| `priorityTask`     | ChoiceField    | Priorität (z. B. low, medium, high)              |
| `status`           | IntegerField   | Status (To Do, In Progress, Await Feedback, Done)|
| `timeDeadlineTask` | DateField      | Fälligkeitsdatum                                 |
| `subTasks`         | ManyToMany     | Verknüpfte Unteraufgaben                         |

### 3. **SubTask**
| Feld           | Typ          | Beschreibung                                      |
|----------------|--------------|---------------------------------------------------|
| `id`           | Integer      | Primärschlüssel                                   |
| `subTaskName`  | CharField    | Name der Unteraufgabe                             |
| `statusSubTask`| BooleanField | Status (True = abgeschlossen, False = offen)      |

--- 

Dieses README deckt die grundlegende Nutzung und API-Struktur des Backends ab.
