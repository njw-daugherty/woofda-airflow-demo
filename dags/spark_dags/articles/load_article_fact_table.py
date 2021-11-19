import os

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, explode, to_date, trim

conf = SparkConf()
conf.set("spark.jars.ivy", "/opt/airflow/ivy")
conf.set("spark.jars.packages", "org.postgresql:postgresql:42.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.901,org.apache.hadoop:hadoop-aws:3.3.1")
conf.set("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider")
# conf.set('spark.hadoop.fs.s3a.access.key', "")
# conf.set('spark.hadoop.fs.s3a.secret.key', "")

spark = (
    SparkSession
    .builder
    .config(conf=conf)
    .appName("load_article_fact_table")
    .getOrCreate()
)

SUBJECT = os.getenv("SUBJECT")
LOGICAL_DATE = os.getenv("LOGICAL_DATE")

DESTINATION_HOST = os.getenv("DESTINATION_HOST")
DESTINATION_DATABASE = os.getenv("DESTINATION_DATABASE")
DESTINATION_USER = os.getenv("DESTINATION_USER")
DESTINATION_PASSWORD = os.getenv("DESTINATION_PASSWORD")
DESTINATION_TABLE = os.getenv("DESTINATION_TABLE")

prod_table = (spark.read
    .format("jdbc")
    .option("driver", "org.postgresql.Driver")
    .option("url", f"jdbc:postgresql://{DESTINATION_HOST}/")
    .option("dbtable", DESTINATION_TABLE)
    .option("user", DESTINATION_USER)
    .option("password", DESTINATION_PASSWORD)
    .load()
)

prod_table.show()

""" prod_table
+----------+-----+---+---+------------+----------+----------+---------------+------------+--------------+------------+
|article_id|title|doi|uri|publisher_id|journal_id|print_issn|electronic_issn|date_created|date_deposited|date_indexed|
+----------+-----+---+---+------------+----------+----------+---------------+------------+--------------+------------+
+----------+-----+---+---+------------+----------+----------+---------------+------------+--------------+------------+
"""

candidate_records = spark.read.json(f"s3a://dbs-airflow-demo-datalake/raw/crossref/articles/{SUBJECT}/articles-{LOGICAL_DATE}.json")
candidate_records.show()

"""candidate_records
+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+---------------+----------+
|                 DOI|                ISSN|                 URL|              author|     container-title|             created|           deposited|             indexed|           issn-type|           publisher|           reference|               title|           type|article_id|
+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+---------------+----------+
|10.1007/s11007-02...|[1387-2842, 1573-...|http://dx.doi.org...|[{null, [], null,...|[Continental Phil...|{[[2021, 11, 16]]...|{[[2021, 11, 16]]...|{[[2021, 11, 16]]...|[{print, 1387-284...|Springer Science ...|[{10.1017/S135824...|[Merleau-Ponty’s ...|journal-article|         0|
|10.3366/jsp.2021....|[1479-6651, 1755-...|http://dx.doi.org...|[{null, [{College...|[Journal of Scott...|{[[2021, 11, 16]]...|{[[2021, 11, 16]]...|{[[2021, 11, 16]]...|[{print, 1479-665...|Edinburgh Univers...|[{null, null, ‘Ar...|[Elizabeth Hamilt...|journal-article|         1|
"""

candidate_records = (
    candidate_records.select(
        col("DOI").alias("doi"),
        col("URL").alias("uri"),
        to_date(col("created")["date-time"], "yyyy-MM-dd'T'HH:mm:ss'Z'").alias("date_created"),
        to_date(col("deposited")["date-time"], "yyyy-MM-dd'T'HH:mm:ss'Z'").alias("date_deposited"),
        to_date(col("indexed")["date-time"], "yyyy-MM-dd'T'HH:mm:ss'Z'").alias("date_indexed"),
        concat_ws(",", col("title")).alias("title"),
    )
)
candidate_records.show()
"""
+--------------------+--------------------+------------+--------------+------------+--------------------+
|                 doi|                 uri|date_created|date_deposited|date_indexed|               title|
+--------------------+--------------------+------------+--------------+------------+--------------------+
|10.1007/s11007-02...|http://dx.doi.org...|  2021-11-16|    2021-11-16|  2021-11-16|Merleau-Ponty’s p...|
|10.3366/jsp.2021....|http://dx.doi.org...|  2021-11-16|    2021-11-16|  2021-11-16|Elizabeth Hamilto...|
+--------------------+--------------------+------------+--------------+------------+--------------------+
"""

new_records = (
    candidate_records.join(
        prod_table,
        ["title", "doi", "uri"],
        "leftanti"
    )
)

new_records.show()

(new_records.write
    .format("jdbc")
    .option("driver", "org.postgresql.Driver")
    .option("url", f"jdbc:postgresql://{DESTINATION_HOST}/")
    .option("dbtable", DESTINATION_TABLE)
    .option("user", DESTINATION_USER)
    .option("password", DESTINATION_PASSWORD)
    .save(mode="append")
)

