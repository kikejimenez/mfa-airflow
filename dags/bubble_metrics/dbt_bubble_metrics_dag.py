from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.models import Variable


default_args = {
    "start_date": days_ago(1),
}


@dag(schedule_interval="@daily", default_args=default_args, catchup=False)
def dbt_dag():
    @task
    def install_requirements():
        import subprocess

        # Path to your requirements.txt file
        requirements_path = "/opt/requirements.txt"

        # Command to install packages from requirements.txt
        install_command = f"pip install -r {requirements_path}"

        try:
            # Execute the command
            subprocess.run(install_command, check=True, shell=True)
            print("Successfully installed packages from requirements.txt")
        except subprocess.CalledProcessError as e:
            # Handle exceptions if the installation fails
            print(f"Failed to install packages: {e}")

        # Additional commands can be added here if necessary
        # ...

    @task
    def run_dbt():
        import subprocess
        import os

        # Fetch the dbt project path from env Variables
        dbt_project_path = "/opt/dbt"

        # Fetch the dbt environment flag from env Variables
        dbt_env = Variable.get("DBT_PROFILE_ENV", default_var="dev")

        # Set the DBT_ENV environment variable for the subprocess
        env = os.environ.copy()
        env["DBT_ENV"] = dbt_env

        # Run the dbt command with the specified environment

        subprocess.run(["dbt", "run"], cwd=dbt_project_path, env=env)

    # Use the task in your DAG
    install_reqs = install_requirements()
    dbt_task = run_dbt()


dbt_dag_instance = dbt_dag()
