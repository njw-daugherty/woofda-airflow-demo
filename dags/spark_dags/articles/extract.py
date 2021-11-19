def get_articles(ds: str, subject_keyword: str, s3_key: str, bucket: str, conn_id: str) -> None:
    """Call the API to get the articles created on a certain day. Writes the result to S3 bucket"""
    import json
    import os

    from airflow.providers.amazon.aws.hooks.s3 import S3Hook
    from crossref.restful import Works

    works = Works()

    articles = (
        works.query(container_title=subject_keyword)
        .filter(type="journal-article")
        .filter(from_created_date=ds, until_created_date=ds)
        .select(
            "DOI",
            "ISSN",
            "issn-type",
            "URL",
            "author",
            "container-title",
            "created",
            "deposited",
            "indexed",
            "publisher",
            "reference",
            "title",
            "type"
        )
    )

    cleaned_subject_name = subject_keyword.lower().replace(" ", "_")

    file_path = "/opt/airflow/output/{}/".format(cleaned_subject_name)

    if not os.path.exists(file_path):
        os.mkdir(file_path)


    with open(file_path + "articles-{}.json".format(cleaned_subject_name), "w+") as json_file:
        json.dump([article for article in articles], json_file)

    

    hook = S3Hook(aws_conn_id=conn_id)
    hook.load_file(
        file_path, s3_key, bucket_name=bucket,  replace=True, acl_policy="public-read"
    )