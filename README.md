# Airflow-Kafka-Spark-Cassandra-Data-Engineering-Workflow
This is a project to use Apache Airflow, Apache Kafka, Apache Spark and Cassandra.

The project uses Apache Airflow to create a DAG which when triggered, gets information from an API about different anonymous users. This information is then streamed inside a Kafka Topic, from which Spark performs a read operation using a Master-Worker architecture and writes the final data inside Cassandra Database.
