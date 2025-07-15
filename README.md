A simple CRUD API built using FastAPI – a modern, high-performance web framework for building APIs with Python 3. This project serves as a great starting point for beginners learning backend API development with FastAPI, SQLAlchemy, and Pydantic.

Features
FastAPI framework

CRUD operations for "Post" resources

SQLite database with SQLAlchemy ORM

Pydantic models for request/response validation

Modular project structure with routers

Interactive Swagger UI and ReDoc API docs

Folder Structure
graphql
Copy
Edit
basicFastAPI/
├── app/
│   ├── __init__.py
│   ├── main.py               # Entry point for FastAPI app
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── database.py           # Database configuration
│   ├── routers/
│   │   └── post.py           # Routes for CRUD operations
├── requirements.txt
└── README.md
How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/neetjainnn/basicFastAPI.git
cd basicFastAPI
Create and activate a virtual environment:

bash
Copy
Edit
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Start the FastAPI server:

bash
Copy
Edit
uvicorn app.main:app --reload
Open your browser and test the API:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Example Endpoints
Method	Endpoint	Description
GET	/posts/	Retrieve all posts
POST	/posts/	Create a new post
GET	/posts/{id}	Retrieve a post by ID
PUT	/posts/{id}	Update a post
DELETE	/posts/{id}	Delete a post

Tech Stack
Python 3.10+

FastAPI

Uvicorn (ASGI server)

SQLAlchemy

Pydantic

