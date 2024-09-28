# Django Test Task with JWT Authentication
  This is a Django project implementing JWT authentication using Simple JWT. Users can create threads, manage messages, and interact with the API using token-based authentication.

Getting Started

1. Clone the Repository

```
git clone https://github.com/YuriiYukh/iSi_tech_test_task.git
cd django-test-task
```

2. Set Up Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

3. Install Dependencies

```
pip install -r requirements.txt
```

4. Database Configuration
   Copy SQLite db file with test_data into the working dir

5. Apply Migrations

```
python manage.py migrate
```

6. Create a Superuser (Optional)

```
python manage.py createsuperuser
```

7. Run the Development Server

```
python manage.py runserver
Now visit http://127.0.0.1:8000/
```

JWT Authentication
This project uses JWT for authentication.

Obtain Access and Refresh Tokens

```
Endpoint: /api/token/
Method: POST
Body:
{
  "username": "your_username",
  "password": "your_password"
}
```

You will get two tokens:

```
access: The token for authenticated requests.
refresh: Token to refresh the access token.
```

Refresh the Access Token

```
Endpoint: /api/token/refresh/
Method: POST
Body:
{
  "refresh": "your_refresh_token"
}
```

# Endpoints
## JWT Authentication:

/api/token/
/api/token/refresh/

## Thread Management:

POST /threads/
PATCH/PUT/DELETE by id /threads/{thread_id}/
GET /threads/list_for_user/?user_id=1

## Message Management:

POST /messages/    <- path thread: {thread_id} in body here to create message for a specific thread
GET /messages/thread/1/messages/
PATCH /messages/1/mark-as-read/
GET /messages/unread-count/?user_id=1
