#!/usr/bin/env python3
#
# Query AWS Athena using SQL
# Requirements:
# > pip3 install boto3 botocore retrying

import os
import sys
import csv
import boto3
#from retrying import retry

# configuration
s3_bucket = 'ashuemployeebkt'       # S3 Bucket name
s3_ouput  = 's3://'+ s3_bucket   # S3 Bucket to store results
database  = 'sampledb'  # The database to which the query belongs

# init clients
athena = boto3.client('athena', region_name='us-east-1')
s3     = boto3.resource('s3')


def poll_status(_id):
    result = athena.get_query_execution( QueryExecutionId = _id )
    import pdb;pdb.set_trace()
    state  = result['QueryExecution']['Status']['State']
    if state != 'FAILED':
        return result
    """if state == 'SUCCEEDED':
        return result
    elif state == 'FAILED':
        return result"""

def run_query(query, database, s3_output):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': s3_output,
    })

    QueryExecutionId = response['QueryExecutionId']
    result = poll_status(str(QueryExecutionId))
    if result['QueryExecution']['Status']['State'] != 'FAILED':
        print("Query SUCCEEDED: {}".format(QueryExecutionId))

        s3_key = QueryExecutionId + '.csv'
        local_filename = QueryExecutionId + '.csv'

        # download result file
        try:
            s3.Bucket(s3_bucket).download_file(s3_key, local_filename)
        except:
            print("The object does not exist.")
        # read file to array
        rows = []
        with open(local_filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)

        # delete result file
        if os.path.isfile(local_filename):
            os.remove(local_filename)

        return rows

if __name__ == '__main__':
    # SQL Query to execute
    query = ("""
        SELECT *
        FROM sampledb.emp
        LIMIT 20
    """)

    print("Executing query: {}".format(query))
    result = run_query(query, database, s3_ouput)

    print("Results:")
    print(result)
