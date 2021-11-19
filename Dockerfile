FROM apache/airflow:2.2.1-python3.7
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    default-jdk \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN curl -o /usr/local/src/spark.tgz https://dlcdn.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz \
    && mkdir -p /opt/spark \
    && tar zxvf /usr/local/src/spark.tgz -C /opt/spark
USER airflow
RUN pip install --no-cache-dir apache-airflow-providers-amazon \
    apache-airflow-providers-apache-spark \
    apache-airflow-providers-apache-livy \
    apache-airflow-providers-cncf-kubernetes \
    apache-airflow-providers-databricks \
    apache-airflow-providers-docker \
    apache-airflow-providers-postgres
    
