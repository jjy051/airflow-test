from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

from datetime import datetime

default_args = {
    'start_date': datetime(2021, 1, 1)
}

with DAG('parallel_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    task1 = BashOperator(
        task_id='task_1',
        bash_command='sleep 3'
    )

    with TaskGroup('processing_tasks') as processing_tasks:
        task2 = BashOperator(
            task_id='task_2',
            bash_command='sleep 3'
        )

        with TaskGroup('spark_tasks') as spark_tasks:
            task3 = BashOperator(
                task_id='task_3',
                bash_command='sleep 3'
            )

        with TaskGroup('flink_tasks') as flink_tasks:
            task3 = BashOperator(
                task_id='task_3',
                bash_command='sleep 3'
            )

    task4 = BashOperator(
        task_id='task_4',
        bash_command='sleep 3'
    )

    task1 >> processing_tasks >> task4
