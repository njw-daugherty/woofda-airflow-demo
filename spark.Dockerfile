FROM bitnami/python:3.7 as build

FROM bitnami/spark:3

COPY --from=build /opt/bitnami/python/ /opt/bitnami/python/

RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.0.3/hadoop-aws-3.3.1.jar \
    --output /opt/bitnami/spark/jars/hadoop-aws-3.3.1.jar