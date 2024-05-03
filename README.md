# FastAPI Boilerplate

# Features
## Event Management Feature

### Overview
This feature enhances the existing project structure to manage a collection of events. Each event has specific properties and can be manipulated through a REST API.

### Entities
#### Event
- **id** (unique identifier, auto-generated)
- **title** (string, required)
- **description** (string, optional)
- **status** (enum, required: ['TODO', 'IN_PROGRESS', 'COMPLETED'])
- **createdAt** (date, auto-generated)
- **updatedAt** (date, auto-generated)
- **startTime** (datetime)
- **endTime** (datetime)
- **invitees** (list of Users)

#### Users
- **Id**
- **name**
- **events** (list of strings)

### REST API
#### Endpoints
1. **Create a new event**
   - Method: POST
   - Path: `/event/`
   - Request Body:
     ```json
     {
       "title": "Event Title",
       "description": "Event Description",
       "status": "TODO",
       "startTime": "2024-05-03T14:00:00Z",
       "endTime": "2024-05-03T15:00:00Z",
       "invitees": ["user_id_1", "user_id_2"]
     }
     ```
   - Response: True or False

2. **Retrieve an event by its id**
   - Method: GET
   - Path: `/events/{id}`
   - Response:
     ```json
     {
       "id": "12345",
       "title": "Event Title",
       "description": "Event Description",
       "status": "TODO",
       "startTime": "2024-05-03T14:00:00Z",
       "endTime": "2024-05-03T15:00:00Z",
       "invitees": ["user_id_1", "user_id_2"]
     }
     ```

3. **Delete an event by its id**
   - Method: DELETE
   - Path: `/events/{id}`
   - Response: True or False

4. **Merge overlapping events**
   - Method: POST
   - Path: `/events/merge-all/{uid}`
   - Response: List of json files, each present one new merged event

## Run

### Launch docker
```shell
> docker-compose -f docker/docker-compose.yml up
```

### Install dependency
```shell
> poetry shell
> poetry install
```

### Apply alembic revision
```shell
> alembic upgrade head
```

### Run server
For Windows Powershell:
```shell
> python3 main.py --env local;dev;prod --debug
```
For Mac or Linux:
Firstly modify the following line in Makefile:
```shell
set ENV=test&& pytest tests -s
```
to
```shell
ENV=test && pytest tests -s
```
then run
```shell
> python3 main.py --env local|dev|prod --debug
```


### Run test codes
```shell
> make test
```
