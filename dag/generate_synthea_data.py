from airflow.sdk import DAG, task, Asset, Metadata
import pendulum
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.standard.operators.bash import BashOperator
import random 
from docker.types import Mount

with DAG(
    dag_id = 'generate_synthea_data',
    start_date = pendulum.parse('2026-04-24',tz = 'Asia/Bangkok'),
    schedule = None,
    max_active_runs = 1
) as dag:

    state_list = [
        "California","New York","Texas","Florida","Hawaii",
        "Nevada","Alaska","Illinois","Massachusetts","Colorado"
    ]

    @task()
    def generate_command(state):
            seed = 0
            population = random.randint(1_000,5_000)

            return f'java -jar /home/ubuntu/synthea-with-dependencies.jar "{state}" -p {population} -c /home/ubuntu/synthea/synthea.properties'

    t_generate_command = generate_command.expand(state = state_list)

    run_synthea_docker = DockerOperator.partial(
        task_id = 'run_synthea_docker',
        max_active_tis_per_dag = 1,
        image = 'synthea',
        mounts= [
            Mount(source="{{ var.value.synthea_output_path }}/batch{{ ti.map_index }}", target='/home/ubuntu/output', type= 'bind'),
            Mount(source="{{ var.value.synthea_config_path }}", target='/home/ubuntu/synthea', type= 'bind'),
        ],
        mount_tmp_dir=False,
        auto_remove='force',
        docker_url='tcp://localhost:2375',
        network_mode='pipeline-network',
        api_version="auto",
    ).expand(
        command = t_generate_command
    )

    t_generate_command >> run_synthea_docker