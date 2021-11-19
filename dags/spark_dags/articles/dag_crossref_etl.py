import datetime
import sys

sys.path.append("/opt/airflow/dags/spark_dags/articles")

from extract import get_articles

from airflow.models.dag import DAG

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {"owner": "nathan.watson@daugherty.com"}

subjects = [
    "Economics",
    "Information Technology",
    "Philosophy",
]

with DAG(
    "spark_crossref_etl__1.0.5",
    "Retrieves indexed articles from the CrossRef API and writes them to an Amazon S3 bucket",
    schedule_interval="@daily",
    start_date=datetime.datetime(2021, 11, 18),
    default_args=default_args,
    max_active_runs=1,
    template_searchpath="/opt/airflow/dags/spark_dags/articles",
    tags=["CrossRef", "Spark", "Spark-Submit", "Demo"],
) as dag:

    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")

    etl_tasks = []

    for subject in subjects:

        subject_name = subject.lower().replace(" ", "_")

        task_get_articles = PythonOperator(
            task_id="get_{}_articles".format(subject_name),
            python_callable=get_articles,
            op_kwargs={
                "subject_keyword": subject,
                "s3_key": "raw/crossref/articles/{}/".format(subject_name) + "articles-{{ds}}.json",
                "bucket": "dbs-airflow-demo-datalake",
                "conn_id": "nathan_aws_account",
            },
        )

        # task_staging_ddl = PostgresOperator(
        #     task_id="create_{}_staging_tables".format(subject_name),
        #     sql="stage_ddl.sql",
        #     postgres_conn_id="data_warehouse",
        #     params={"subject": subject_name},
        # )

        task_stage_author_dimension = SparkSubmitOperator(
            application="/opt/airflow/dags/spark_dags/articles/stage_author_dimension.py",
            conn_id="local_spark_cluster",
            task_id="stage_{}_author_dimension".format(subject_name),
            packages="org.postgresql:postgresql:42.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.901,org.apache.hadoop:hadoop-aws:3.3.1",
            env_vars={
                "SUBJECT": subject_name,
                "LOGICAL_DATE": "{{ds}}",
                "DESTINATION_HOST": "{{ conn.data_warehouse.host }}",
                "DESTINATION_DATABASE": "{{ conn.data_warehouse.schema }}",
                "DESTINATION_TABLE": "staging.author_{{ ts_nodash }}_" + subject_name,
                "DESTINATION_USER": "{{ conn.data_warehouse.login }}",
                "DESTINATION_PASSWORD": "{{ conn.data_warehouse.password }}",
            },
            conf={"spark.jars.ivy": "/opt/airflow/ivy"},
            driver_memory="2G",
        )

        # task_spark_submit = SparkSubmitOperator(
        #     application="/opt/airflow/dags/spark_dags/articles/transform.py",
        #     conn_id="local_spark_cluster",
        #     task_id="transform_{}_articles".format(subject_name),
        #     packages="org.postgresql:postgresql:42.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.901,org.apache.hadoop:hadoop-aws:3.3.1",
        #     env_vars={"SUBJECT": subject_name, "DATE": "{{ds}}"},
        #     conf={"spark.jars.ivy": "/opt/airflow/ivy"},
        # )

        start >> task_get_articles >> task_stage_author_dimension >> end
