from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.models import Variable


default_args = {
    "start_date": days_ago(1),
}


@dag(schedule_interval="@daily", default_args=default_args, catchup=False)
def dbt_dag():
    @task
    def run_dbt():
        import subprocess
        import os

        # Fetch the dbt project path from env Variables
        dbt_project_path = os.getenv("DBT_PROJECT_PATH", "if-no-dbt-path/make-it-fail")

        # Fetch the dbt environment flag from env Variables
        dbt_env = Variable.get("DBT_PROFILE_ENV", default_var="dev")

        # Set the DBT_ENV environment variable for the subprocess
        env = os.environ.copy()
        env["DBT_ENV"] = dbt_env

        # Run the dbt command with the specified environment

        subprocess.run(["dbt", "run"], cwd=dbt_project_path, env=env)

    dbt_task = run_dbt()


dbt_dag_instance = dbt_dag()
