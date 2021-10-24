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
One example of data pipeline (one DAGs) - let follow below steps and make data pipeline
- creating table -> is-api-available -> extending -> processing-use -> 
- what is it? when new user comes in, sense that and process and store user info to destination (?)

#### 1) creating table
- make python script user_processing.py in dags folder
- let create table using sqlite operator in user_processing.py
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
- set sqlite connection on Airflow Web UI

```
pip install apache-airflow-providers-sqlite ## install airflow provider of sqlite. refer airflow doc. may already be installed from intial installing Airflow..
# next, make a new sqltie connection named 'db_sqlite' in Airflow
```

- after that, do test airflow tasks!

`airflow tasks test user_processing creating_table 2020-01-01`

- one more things to do just for check again
```
sqlite3 airflow.db ## connect to sqlite3 in airflow.db
sqlite>.tables; ## see the tables in airflow.db in sqlite cmd
sqlite>select * form users; ## test query in sqlite cmd
```

#### 2) is_api_available
- add HttpSensor Operator in existing python script like below

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
- Like 1) step, install airflow provider of Http and add new connection of Http api communication from Airflow Web connection configuration

#### 3) 


