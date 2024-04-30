main branch

docker-based-eltpipeline

Acknowledgement : https://www.youtube.com/watch?v=PHsC_t0j1dU&list=PLYuYLXPORU73j927mJZwgDrMfRaooXQVZ&index=2

Data Engineering Course for Beginners by freeCodeCamp.org

setting up a Docker-based Extract, Load, Transform (ELT) process using Docker Compose and Python scripts to transfer data from one PostgreSQL database to another.

1. Docker Compose Configuration:

Defines two PostgreSQL services (source_postgres and destination_postgres) and an ELT script service (elt_script) [ total 3 containers]

Sets up a custom network (elt_network) for the services to communicate.

2. Python Script (elt_script.py):

Defines a function wait_for_postgres to wait until PostgreSQL is ready to accept connections.

Waits for the source PostgreSQL database (source_postgres) to be ready.

Defines configurations for the source and destination PostgreSQL databases.

Uses pg_dump to dump the source database into a SQL file (data_dump.sql).

Uses psql to load the dumped SQL file into the destination database.

The script is set to run as the default command for the elt_script service.

3. Dockerfile for ELT Script:

Installs PostgreSQL client tools.

Copies the Python script into the container.

Sets the default command to run the Python script.

4. SQL Data:

Defines tables (users, films, film_category, actors, film_actors) and inserts data into them.# docker-based-etl-pipeline-dbl

Destination database name is destination_db

5. To verify the data is moved to psql :

>> docker exec -it <dest_postgres_container_id> psql -h <hostname : destination_postgres> -U <user: postgres> -d <destinaiton db name : destination_db>

>> \l : list all db

>> \c destination_db : use destination database

>> \dt : show all tables

>> select * from actors;

dbt branch

data is already there in destination_db which will now be the source for all the actions. DBT runs after this ( when data is already in the destination_db)

in ELT , it is used to perform "T" transformations on the data stored in the data warehouse.

Defining some terms:

Models : they are just files where we query the data. Example: films.sql Model

select * from {{source('destination_db', 'films')}}

Schema.yml : they tell you how data is organised in the db.

sources.yml : specifying RAW data from destination_db

dbt profile.yml File ( created when we do dbt_init during the setup )

To verify our dbt pipeline was successfully created, we need to check if the " film_ratings" table exists in our db.

>> docker exec -it <dest_postgres_container_id> psql -h <hostname : destination_postgres> -U <user: postgres> -d <destinaiton db name : destination_db>

>> \l : list all db

>> \c destination_db : use destination database

>> \dt : show all tables

***EDIT  : This was fixed by adding a condition to dbt container "depends on" 
** On running docker compose up , there might be an error which would translate to dbt not being able to connect to destination_db. For this, do 
>> docker compose up 
>> docker compose dbt 

 WHY? 
 it seems like the dbt service depends on the destination_postgres service. If you simply run docker-compose up, Docker will start all services in the docker-compose.yaml file concurrently, which means dbt might start running before destination_postgres is fully ready to accept connections.

When you run docker-compose up followed by docker-compose up dbt-1, the first command starts all the services including destination_postgres, and the second command starts dbt-1 specifically. At the time dbt-1 starts, destination_postgres is probably fully ready, hence we do not encounter any connection issues.

### Branch cron 
Cron job is basically to run the pipeline automatically at a particular time or during a particular interval.

We just made changes in start.sh file & Dockerfile. 