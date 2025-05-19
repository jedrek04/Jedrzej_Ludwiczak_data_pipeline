from google.cloud import storage, bigquery
import functions_framework
from flask import jsonify
import io
import csv

@functions_framework.http
def load_to_bq(request):
    bucket_name = 'platform_assignment_bucket'
    file_name = 'ga4_public_dataset.csv'
    cleaned_file_name = 'cleaned_ga4_public_dataset.csv'
    dataset_id = 'platform_assignment_dataset'
    table_id = 'Jedrzej_Ludwiczak_ga4_table'

    # initializing storage and bigquery clients
    storage_client = storage.Client()
    bq_client = bigquery.Client()

    # getting all blobs (files) from the bucket
    bucket = storage_client.bucket(bucket_name)
    blobs = list(bucket.list_blobs())

    # collecting file names
    file_names = [blob.name for blob in blobs]
    last_updated = max(blob.updated for blob in blobs) if blobs else None

    # trying to find the desired csv file
    matching_blob = next((blob for blob in blobs if blob.name == file_name), None)

    # error message if file isnt there
    if not matching_blob:
        return jsonify({
            'message': f'{file_name} not found',
            'files': file_names,
            'last_updated': str(last_updated)
        }), 404

    # downloading the file contents as bytes and decoding it to text
    raw_bytes = matching_blob.download_as_bytes()
    raw_text = raw_bytes.decode('utf-8')

    # setting up input and output buffers for processing the csv in memory
    input_io = io.StringIO(raw_text)
    output_io = io.StringIO()

    # using csv reader to parse input line by line
    reader = csv.reader(input_io)
    writer = csv.writer(output_io, quoting=csv.QUOTE_ALL)

    for row in reader:
        writer.writerow(row)

    # uploading the cleaned version of the file back to the same bucket
    cleaned_blob = bucket.blob(cleaned_file_name)
    cleaned_blob.upload_from_string(output_io.getvalue(), content_type='text/csv')

    # making sure the dataset exists in bigquery
    dataset_ref = bq_client.dataset(dataset_id)
    try:
        bq_client.get_dataset(dataset_ref)
    except Exception:
        bq_client.create_dataset(bigquery.Dataset(dataset_ref))

    # setting the uri of the cleaned csv file
    uri = f'gs://{bucket_name}/{cleaned_file_name}'
    table_ref = dataset_ref.table(table_id)

    # configuring how the csv should be loaded into bigquery
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        quote_character='"',
        allow_quoted_newlines=True
    )

    try:
        # starting the load job and waiting for it to complete
        load_job = bq_client.load_table_from_uri(uri, table_ref, job_config=job_config)
        load_job.result()
    except Exception as e:
        # returning error message if the load fails
        return jsonify({
            'message': 'BigQuery load failed',
            'error': str(e)
        }), 500

    # returning success response
    return jsonify({
        'message': f'{file_name} cleaned and loaded to {dataset_id}.{table_id}',
        'files': file_names,
        'last_updated': str(last_updated)
    })
