# airflow-test
This is a practice on Airflow, which is
- Builing virtualbox env and setting Airflow on that env
- Installing Airflow using python virtual env
- Coding data pipeline with Airflow
- Based on Udemy lecture (https://www.udemy.com/course/the-complete-hands-on-course-to-master-apache-airflow/)

### First of all, build virtual env using virtualbox
This is optional but highly recommended
- It is very important to make sure that development env is independent and has no conflict with other env setting


### Next, make python virtual env on proper directory

```
python3 -m venv sandbox
source ~/sandbox/bin/activate
```

### Let start to install Airflow and initial setting

Install Airflow
```
pip3 install apache-airflow==2.1.0 \ ## airflow version depends on when you install and constraint 
  --constraint 'git address' ## constraint is ???. It is optional. refer to https://gist.github.com/marclamberti
```


Airflow Inital Setting
```
airflow db init ## airflow metadata initializing
airflow users create -u admin -p admin -f jaeyoung -l jang -r Admin -e admin@airflow.com ## create admin user

airflow webserver ## launch web server. after that we can access airflow web server through localhost:8080
airflow scheduler ## activate airfow scheduler to run DAGs
```

### Construct data pipeline with Airflow
Let's follow below steps and make a data pipeline (one DAG)
- A data pipeline we are going to build is about getting user info through api, processing that info, and fetching the info with proper schema into sqlite db
- It contains several operators, which is 
  - creating table
  - is-api-available
  - extracting user
  - processing user-info
  - storing user
- Also consider task dependency and backfill/catchup method

#### 1) creating table (SqliteOperator)
At first, create table where the final processed data will be stored
- Make python script user_processing.py in dags folder
- Let create table using sqlite operator in user_processing.py
```
from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2020, 1, 1)
}

with DAG('user_processing', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    # Define tasks/operators

    creating_talbe = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL PRIMARY KEY
            );
            '''
    )
```
- To run the above dag scripts, install airflow provider packages
```
pip install apache-airflow-providers-sqlite 
## install airflow provider of sqlite. refer airflow doc. may already be installed from intial installing Airflow..
```

- Make a new sqlite connection named 'db_sqlite' on Airflow Web UI

- After that, do test airflow tasks!

```
airflow tasks test user_processing creating_table 2020-01-01
```

- One more things to do just for check again
```
sqlite3 airflow.db ## connect to sqlite3 in airflow.db
sqlite>.tables; ## see the tables in airflow.db in sqlite cmd
sqlite>select * form users; ## test query in sqlite cmd
```

#### 2) is_api_available (HttpSensor)
Add sensor to check whether api response is valid
- Add HttpSensor in existing python script like below

```
from airflow.providers.http.sensors.http import HttpSensor

with DAG('user_processing', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    ## leave out before sqliteoperator script for simplicity
    
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id = 'user_api',
        endpoint='api/'
    )
```
- Like 1) creating table step, install airflow provider of Http and add new connection of Http api communication from Airflow Web UI
- Remember test a task
```
airflow tasks test user_processing is_api_available 2020-01-01
```

#### 3) extracting user (SimpleHttpOperator)
Get user information through API
- Add SimpleHttpOperator in existing `user_processing.py` dag script
- Install airflow provider packages and add new connection on Airflow Web UI if need
- Test a task

#### 4) processing user-info (PythonOperator)
Process user information into a proper data with schema
- Add PythonOperator in existing `user_processing.py` dag script
- Define python function refered by PythonOperator
- Since PythonOperator is pre-installed packages, don't need to install the packages. And also it does not need to configure a new connection.
- Test a task

#### 5) storing user (BashOperator)
Transfer process data into sqlite3 of airflow.db
- Add BashOperator in existing `user_processing.py` dag script
- Like PythonOperator, it also does not need to install any packages neither configure a connection
- Test a task

#### Consider task dependency and backfill/catchup method
There are several ways to express task dependency, and here show one way
- Add a explicit relations on dependency in a below dag python script
```
creating_table >> is_api_available >> extracting_user >> processing_user >> storing_user
```
- See task dependency of a dag on Airflow Web UI (click a certain dag and see graph view)

Backfill/catchup method
- A dag has two components on schedulling: start_date (or time) and frequency (e.g. daily or hourly)
- If set `catchup=True` then Airflow will run several dag runs from start_time and catches up until the latest time based on frequency being setted up
- In practice, it needs to delete before dag run to work catch-up jobs

#### Refer to dags/user_processing.py as a final dag script

---

### Configuration
DataBases (SQLite, Postgresql)
- SQLite access only one writer at a time
- In contrast, Postgresql access multiple reader and writer at a time
  - thus, you need to change a database supporting multiple reader/writer access when using local or celery executor

Executor (sequential, local, celery)
- SequentialExecutor does not support to process multiple tasks in parallel
- LocalExecutor can process multiple tasks in parallel
- CeleryExecutor can allow multiple tasks in parallel as much as you want through distributing tasks to worker nodes

Concurrency (parallelism, dag_concurrency, max_active_runs_per_dag)
- parallelism is the maximum number of tasks processing at a time
- dag_concurrency is the maximum number of running dags at a time
- max_active_runs_per_dag means the maximum number of dag runs (within a same dag) at a time

### Advanced Concepts
TaskGroup
- Rather than SubDags, TaskGroup is a very useful and powerful concept to grouping complex tasks
- In production, it is really commonly used
- **Refer to dags/parallel_dag.py**

Exchanging Data
- Using external storage to communicate data between tasks
  - A task can refer a data from other tasks through external storage like s3 (or other DB server)
  - It needs to build a certain hook (connection) to push/pull data to external storage


- Using interal default storage (XCOM)
  - If data is a small, we can use a default interal storage for a communication
  - **Refer to dags/xcom_dag.py for a XCOM use case**

Branch, Condition
- To process conditoined data pipeline, it sometimes needs express operator branch whether certain operators start or skip based on criteria
- BranchPythonOperator is a good package to do that
- **Refer to dags/xcom_dag.py**


Trigger Rule
- There are several trigger rules
  - all_success (default), all_failed, one_failed and so on
  - https://airflow.apache.org/docs/apache-airflow/1.10.5/concepts.html?highlight=trigger%20rule
- **Refer to dags/trigger_rule.py**


### 
