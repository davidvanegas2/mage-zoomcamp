import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/de-course-411516-c64d64bd809f.json"

bucket_name = 'terraform_bucket_dfvanegas'
project_id = 'de-course-411516'

table_name = "nyc_taxi_data"

root_path = f"{bucket_name}/{table_name}"


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    data["tpep_pickup_date"] = data["tpep_pickup_datetime"].dt.date

    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=["tpep_pickup_date"],
        filesystem=gcs
    )
