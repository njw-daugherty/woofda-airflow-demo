from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import datetime

docs ="""
# Lorem ipsum
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin condimentum vel metus eu rutrum. Nullam vel tortor in mi rhoncus malesuada. Aenean sollicitudin in est eget pharetra. Sed et metus porttitor, auctor erat et, varius dui. Duis imperdiet tincidunt urna, condimentum ultricies nibh maximus vitae. Morbi velit elit, ultricies tristique rhoncus sit amet, pharetra eleifend lorem. Vivamus in pharetra quam. 

```
print("Hello world")
```

Mauris blandit sem eget quam faucibus lacinia. Morbi congue fringilla ex a porttitor. Aliquam convallis blandit urna at accumsan. Nam ante velit, eleifend sit amet risus id, malesuada lobortis mauris. Curabitur et velit orci. Aenean finibus dictum vulputate. Sed eleifend tincidunt sagittis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras sed commodo elit.
# Donec a nulla
Donec a nulla dignissim, convallis ligula et, facilisis lacus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aliquam lacinia dapibus lectus nec suscipit. Sed tempus tortor eget lectus molestie, vitae interdum justo bibendum. Mauris sed sem orci. Nunc quis blandit lectus. Mauris enim risus, eleifend semper lorem at, semper elementum sapien. Pellentesque justo lorem, vehicula at urna et, cursus accumsan turpis. Curabitur vitae turpis eget arcu imperdiet tristique. Praesent rhoncus a neque in vestibulum. Proin nec nisl venenatis, ultricies felis at, tincidunt dolor. Fusce non cursus erat. Praesent eu odio dui. Cras aliquam lacinia convallis. Donec finibus mauris et mollis fermentum.
"""

default_args = {
    "owner": "nathan.watson@daugherty.com"
}

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
    default_args=default_args,
    tags=["Demo", "Easy", "PythonOperator"],
) as dag:

    dag.doc_md = docs

    run_this = PythonOperator(
        task_id="print_the_context",
        python_callable=get_day_of_week,
    )
    run_this.doc_md = """
    ### Example
    You can also add `markdown` documentation to each task.
    """

    run_this
