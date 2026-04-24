from airflow.sdk import DAG, task, Asset, Metadata
import pendulum
from airflow.providers.docker.operators.docker import DockerOperator
import random 

with DAG(
    dag_id = 'generate_synthea_data',
    start_date = pendulum.parse('2026-04-24',tz = 'Asia/Bangkok'),
    schedule = None
) as dag:


    @task()
    def generate_command():
        seed = 0
        state_list = [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", 
            "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
            "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
            "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
            "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", 
            "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
            "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
            "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
            "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", 
            "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
            ]
        commands_list = []
        for state in state_list:

            population = random.randint(50_000,100_000)
            commands_list.append(
                f'java -jar /home/ubuntu/synthea-with-dependencies.jar "{state}" -p {population} -s {seed} -cs 1777013499694 -c /home/ubuntu/synthea/synthea.properties'
            )
        return commands_list
    
    t1 = generate_command()