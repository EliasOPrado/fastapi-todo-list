# FastAPI - Tasks todo 📝

### How to run the application:
If you have docker installed just run the following command:
```bash
docker compose up --build
```

If you prefer using the default way of start a fastapi application you can follow the next steps:

1 Create a virtual environment and activate it
```bash
python3 -m venv venv && source venv/bin/activate
```
2 Install the packages:
```bash
pip install -r requirements.txt
```
3. Once it is installed you can initiate the wsgi server from fastapi using uvcorn:
```bash
uvicorn main:app --reload
```
ps: remember you should be in the root directory to run this command. 

### The CRUD operations

There are all the CRUD opertions as:
1. `/tasks/` Read all (GET)
2. `/tasks/` Create Todo (POST)
3. `/tasks/{todo_id}` Read Todo (GET)
4. `/tasks/{todo_id}` Update Todo (PUT)
5. `/tasks/{todo_id}` Patch Todo (PATCH)
6. `/tasks/{todo_id}` Delete Todo (DELETE)

For the endpoints above the payload is as follow:
```json
{
  "title": "string",
  "description": "string",
  "completed": true
}
```

### Tests

There have tests for all endpoints and database integration using `pytest`.

To check the functionalities, with the `requirements.txt` installed just write:
```bash
pytes -s
```

To check the tests just go to `test/`.



### Deployment

This service was deployed using `render.com` using docker and a postgres database created on `AWS RDS`.
