# airflow-test
This is a practice on airflow, which is
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


