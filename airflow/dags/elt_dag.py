from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess
import warnings
warnings.filterwarnings("ignore")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

# function to run the script OBVIOUSLY !! 
def run_elt_script():
    script_path = "/opt/airflow/elt/elt_script.py"
    result = subprocess.run(["python", script_path],
                            capture_output=True, text=True)
    
    # we failed something, so we raise an exception
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2023, 4, 30),
    catchup=False,
)

#task 1 - first we want the elt script to run 
t1 = PythonOperator(
    task_id='run_elt_script',
    python_callable=run_elt_script,
    dag=dag,
)

#task 2 - dbt 
# same info as dbt container in docker-compose.yml file
t2 = DockerOperator(
    task_id='dbt_run',
    image='ghcr.io/dbt-labs/dbt-postgres:1.6.0',
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/opt/dbt",
        "--full-refresh"
    ],
    auto_remove=True, #once finished, auto remove container, coz we dont want it open all time
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    
    mounts=[
        Mount(source='/Users/mumukshapant/Downloads/dbt/docker-based-eltpipeline/custom_postgres',
              target='/opt/dbt', type='bind'),
        Mount(source='/Users/mumukshapant/.dbt', target='/root', type='bind'),
        Mount(source='/Users/mumukshapant/Downloads/dbt/docker-based-eltpipeline/elt', target='/opt/airflow/dags', type='bind'),
    ],
    dag=dag
)

t1 >> t2 #order of operation