import os

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, trim

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
    .appName("stage_author_dimension")
    .getOrCreate()
)

SUBJECT = os.getenv("SUBJECT")
LOGICAL_DATE = os.getenv("LOGICAL_DATE")

DESTINATION_HOST = os.getenv("DESTINATION_HOST")
DESTINATION_DATABASE = os.getenv("DESTINATION_DATABASE")
DESTINATION_USER = os.getenv("DESTINATION_USER")
DESTINATION_PASSWORD = os.getenv("DESTINATION_PASSWORD")
DESTINATION_TABLE = os.getenv("DESTINATION_TABLE")

df = (
    spark
    .read
    .json(f"s3a://dbs-airflow-demo-datalake/raw/crossref/articles/{SUBJECT}/articles-{LOGICAL_DATE}.json")
)

df.show()

"""

+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+---------------+----------+
|                 DOI|                ISSN|                 URL|              author|     container-title|             created|           deposited|             indexed|           issn-type|           publisher|           reference|               title|           type|article_id|
+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+---------------+----------+
|10.1007/s11007-02...|[1387-2842, 1573-...|http://dx.doi.org...|[{null, [], null,...|[Continental Phil...|{[[2021, 11, 16]]...|{[[2021, 11, 16]]...|{[[2021, 11, 16]]...|[{print, 1387-284...|Springer Science ...|[{10.1017/S135824...|[Merleau-Ponty’s ...|journal-article|         0|
|10.3366/jsp.2021....|[1479-6651, 1755-...|http://dx.doi.org...|[{null, [{College...|[Journal of Scott...|{[[2021, 11, 16]]...|{[[2021, 11, 16]]...|{[[2021, 11, 16]]...|[{print, 1479-665...|Edinburgh Univers...|[{null, null, ‘Ar...|[Elizabeth Hamilt...|journal-article|         1|

"""

authors_exploded = (
    df.select(
        explode(col("author")).alias("author"),
    )
)

authors_exploded.show(truncate=False)

authors = (
    authors_exploded
    .select(
        trim(col("author")["given"]).alias("given_name"),
        trim(col("author")["family"]).alias("family_name"),
        trim(col("author")["affiliation"][0]["name"]).alias("organization"),
        trim(col("author")["ORCID"]).alias("orc_id")
    )
    .dropna(subset=["given_name", "family_name"])
    .dropDuplicates(["given_name", "family_name", "orc_id"])
)

authors.show()

(authors.write
    .format("jdbc")
    .option("driver", "org.postgresql.Driver")
    .option("url", f"jdbc:postgresql://{DESTINATION_HOST}/")
    .option("dbtable", DESTINATION_TABLE)
    .option("user", DESTINATION_USER)
    .option("password", DESTINATION_PASSWORD)
    .save(mode="overwrite")
)

