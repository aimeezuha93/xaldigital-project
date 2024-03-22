## xaldigital-project

For the development of this challenge and particularly the API, I decided to use the Python Flask framework.

Please noted that this is the first time I have developed an API because I have always focused on developing ETL.

> Note:
Things I decided not to focus on
>- ER design: Because it is indicated that various data sample files would be attached to be able to design and build the data models, with the only file that was attached it cannot be done.
>- Implement CI/CD.
>- Implement a mechanism to create or update the schema.

## Steps

1. Clone this repository.

```BASH
git clone https://github.com/aimeezuha93/xaldigital-project.git
```
2. Located within the repository at the level where the `docker-compose.yml` file is located.
3. Build the image.
```BASH
docker-compose -f docker-compose.yml up --build
```
4. Run the following command to validate that the containers were created correctly.
```BASH
docker ps
```
The output should look like this:
```
CONTAINER ID   IMAGE                    COMMAND                  CREATED       STATUS                 PORTS                            NAMES
5e1df4ed5555   xaldigital-project-api   "flask run --host=0.…"   6 hours ago   Up 6 hours             0.0.0.0:3001->3001/tcp           xaldigital-project-api-1
478c465e17ec   postgres:13              "docker-entrypoint.s…"   6 hours ago   Up 6 hours (healthy)   0.0.0.0:5432->5432/tcp           xaldigital-project-postgres-1
b5b0d149a493   dpage/pgadmin4           "/entrypoint.sh"         6 hours ago   Up 6 hours             443/tcp, 0.0.0.0:15432->80/tcp   xaldigital-project-pgadmin4-1
```

## Part Zero: Services Check

### Flask

1. Go to the following URL http://localhost:3001

When the URL finishes loading, it should return the following

```JSON
{"status": "OK", "message": "This project belongs to user Aimee Zuniga", "version": "1.0.0"}
```

### pgAdmin

You can use any other SQL client software to verify connectivity to Postgres and to validate the operations performed by the API, I decided to use pgAdmin.

1. Go to the following URL http://localhost:15432

2. We can access the pgadmin, with the email and password specified in the .env file (PGADMIN_DEFAULT_EMAIL & PGADMIN_DEFAULT_PASSWORD).

3. Click in Login.
4. Now we can try to connect to PostgreSQL server that we build with Docker. Click on Servers, and go to Object > Create > Server
5. On the tab General: Name: flask_server
6. Click on the tab Connection and put the following information:

- Host name/address: xaldigital-project-postgres-1 *(check the container name by execute docker ps)*
- Port: 5432
- Maintenance database: flask_db
- Username: flask
- Password: flask

7. Click in Save.

## Part One: The Database

Following the comment *"you can decide what you want and do not want to deliver given the time constraints"* within the challenge document, I made the decision not to focus on the way the data was read from the server and uploaded to Postgres and decided to do it in the simplest way possible.

1. First we must copy the *Sample.csv*(it was renamed because parentheses symbols were not accepted by my OS) local data file to the Postgres container.
```BASH
docker cp <file_absolute_local_path> <container_id>:<container_path>
docker cp /Users/bonesknight/Downloads/Sample.csv 61f488766d31:/tmp
```

2. Then we must "enter" the Postgres container in bash mode.
```BASH
docker exec -it <container_name> /bin/sh
docker exec -it xaldigital-project-postgres-1 /bin/sh
```

3. Before loading the data we need to create the table.
```BASH
psql flask_db -U flask -c "CREATE TABLE public.employees(first_name VARCHAR(60),last_name VARCHAR(100),company_name VARCHAR,address TEXT,city VARCHAR(50),state TEXT CHECK (char_length(state) = 2 AND state ~ '^[A-Za-z]+$'),zip INT,phone1 VARCHAR(16),phone2 VARCHAR(16),email VARCHAR(50),department VARCHAR(30));"
```
Note that during the table creation, the 2 validations requested for the status column are indicated.

4. Now we must execute Postgres' own COPY command to load the data to the database.
```BASH
psql flask_db -U flask -c "\copy public.employees (first_name,last_name,company_name,address,city,state,zip,phone1,phone2,email,department) FROM '/tmp/Sample.csv' DELIMITER ',' CSV HEADER;"
```

4. Finally we need to verify that the table has been created and contains the desired data within pgAdmin.

## Part Two: The API

To validate that our API is receiving requests, 2 welcome requests have been created.
They can be tested making a GET request to / or /status route using a tool like Postman.

```HTTP
GET http://127.0.0.1:3001/
GET http://127.0.0.1:3001/status
```

The response should look as follows

```JSON
{
    "status": "OK",
    "message": "This project belongs to user Aimee Zuniga",
    "version": "1.0.0"
}
```

```JSON
{
    "status": "OK"
}
```

### Requests

1. Retrive a particular record.
#### REQUEST
```
GET http://127.0.0.1:3001/employees/lperin@perin.org
```

#### RESPONSE.
```JSON
{
    "status": "success",
    "data": [
        {
            "first_name": "Lavera",
            "last_name": "Perin",
            "company_name": "Abc Enterprises Inc",
            "address": "678 3rd Ave",
            "city": "Miami",
            "state": "FL",
            "zip": 33196,
            "phone1": "305-606-7291",
            "phone2": "305-995-2078",
            "email": "lperin@perin.org",
            "department": "Sales"
        }
    ]
}
```

2. Insert a new record.
#### REQUEST
```
POST http://127.0.0.1:3001/employees
```
Body
```JSON
{
   "data":{
      "first_name":"Pepito",
      "last_name":"Piedras",
      "company_name":"La Rojeña",
      "address":"Colinas de Santa Monica 1234",
      "city":"Mateos",
      "state":"NL",
      "zip":9568,
      "phone1":"55-89-02-76",
      "phone2":"56-30-84-63",
      "email":"pedrito_piedras@yahoo.com",
      "department":"Operations"
   }
}
```

#### RESPONSE.
```JSON
{
    "status": "success",
    "data": {
        "message": "Employee inserted successfully"
    }
}
```

3. Update a particular record.
#### REQUEST
```
PUT http://127.0.0.1:3001/employees/jamal@vanausdal.org
```
Body
```JSON
{
   "data":{
      "department": "Marketing"
   }
}
```

#### RESPONSE.
```JSON
{
    "status": "success",
    "data": {
        "message": "Employee updated successfully"
    }
}
```

4. Delete a particular record.
#### REQUEST
```
DELETE http://127.0.0.1:3001/employees/elly_morocco@gmail.com
```

#### RESPONSE.
```JSON
{
    "status": "success",
    "data": {
        "message": "Employee deleted successfully"
    }
}
```