# docker-based-eltpipeline

Acknowledgement : https://www.youtube.com/watch?v=PHsC_t0j1dU&list=PLYuYLXPORU73j927mJZwgDrMfRaooXQVZ&index=2

Data Engineering Course for Beginners by freeCodeCamp.org

 setting up a Docker-based Extract, Load, Transform (ELT) process using Docker Compose and Python scripts to transfer data from one PostgreSQL database to another.
 
# 1. Docker Compose Configuration:
- Defines two PostgreSQL services (source_postgres and destination_postgres) and an ELT script service (elt_script) [ total 3 containers]
- Sets up a custom network (elt_network) for the services to communicate.

#2. Python Script (elt_script.py):
-Defines a function wait_for_postgres to wait until PostgreSQL is ready to accept connections.
-Waits for the source PostgreSQL database (source_postgres) to be ready.
-Defines configurations for the source and destination PostgreSQL databases.
-Uses pg_dump to dump the source database into a SQL file (data_dump.sql).
-Uses psql to load the dumped SQL file into the destination database.
-The script is set to run as the default command for the elt_script service.

#3. Dockerfile for ELT Script:

-Installs PostgreSQL client tools.
-Copies the Python script into the container.
-Sets the default command to run the Python script.

#4. SQL Data:
-Defines tables (users, films, film_category, actors, film_actors) and inserts data into them.