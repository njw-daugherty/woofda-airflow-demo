from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import datetime

def get_day_of_week(ds: str) -> str:
    """
    Takes the execution date and returns the day of the week.
    """
    today: datetime.date = datetime.datetime.strptime(ds, "%Y-%m-%d")
    week_day: str = today.strftime("%A")
    return week_day


with DAG(
    "simple_python_operator_dag",
    description="This demo task gets the day of the week.",
    schedule_interval=datetime.timedelta(hours=1),
    start_date=datetime.datetime(2021, 11, 11),
    tags=["Demo", "Easy", "PythonOperator"],
) as dag:

    run_this = PythonOperator(
        task_id="print_the_context",
        python_callable=get_day_of_week,
    )

    run_this
