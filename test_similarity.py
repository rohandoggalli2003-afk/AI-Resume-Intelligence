from src.semantic_matcher import calculate_similarity


resume = """
I am a Data Engineer with experience in Python,
SQL, PySpark, Azure, Databricks and ETL pipelines.

I have built data processing pipelines using
Apache Spark and worked with cloud-based data platforms.
"""


job_description = """
We are looking for a Data Engineer with experience
in Python, SQL, Apache Spark, Azure and Databricks.

The candidate should have experience building
ETL pipelines and large-scale data processing systems.
"""


score = calculate_similarity(
    resume,
    job_description
)


print("Semantic Similarity Score:", score, "%")