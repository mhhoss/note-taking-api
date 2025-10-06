![Developing](https://img.shields.io/badge/Status-Developing-red)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mahdi%20Hosseini-blue)](https://www.linkedin.com/in/mahosseini/)


# NOTE-TAKING-API

A simple **CRUD RESTful API** for managing notes, built with **FastAPI**.

Persistent storage using **SQLite**.

---

## Features
- Get all notes
- Get a single note by ID
- Create a new note
- Update an existing note
- Delete a note

### API Endpoints

| Method | Endpoint        | Description           |
|--------|-----------------|-----------------------|
| GET    | /notes          | Get all notes         |
| GET    | /notes/{id}     | Get note by ID        |
| POST   | /notes          | Create a new note     |
| PUT    | /notes/{id}     | Update a note         |
| DELETE | /notes/{id}     | Delete a note         |

---

## Installation & Setup:

1. Clone the repo:
   ```bash
   git clone https://github.com/mhhoss/note-taking-api.git
   cd note-taking-api
2. Install the [requirements](./requirements.txt).

        pip install -r requirements.txt


### Virtual Environment

1. Create:

        ```bash
        python -m venv venv

2. Activate:

        .\venv\Scripts\Activate.ps1



**Quick run**:

    uvicorn app.main:app --reload

Click [here]([app/main.py](https://github.com/mhhoss/note-taking-api/blob/main/app/main.py)) to view the script.