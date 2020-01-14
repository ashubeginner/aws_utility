#!/usr/bin/env python3

# This will get details of any Glue Dev Endpoint per availability zone and get the Endpoint Alive Duration In Minutes
#!/usr/bin/env python3

import boto3
import datetime
import os

from botocore.exceptions import ClientError

regions = ['ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1',
            'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1',
            'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-east-1', 'us-east-2',
            'us-west-1', 'us-west-2']

def lambda_handler(event, context):
    for region in regions:
        #print(region)
        client = boto3.client('glue', region_name=region)
        endpoint_res = client.get_dev_endpoints()
        dev_endpoints = endpoint_res.get('DevEndpoints')
        print(endpoint_res)
        if dev_endpoints:
            for dev_endpoint in dev_endpoints:
                endpoint_name = dev_endpoint['EndpointName']
                endpoint_az = dev_endpoint['AvailabilityZone']
                created_timestamp = dev_endpoint['CreatedTimestamp'].replace(tzinfo=None)
                lastmodified_timestamp = dev_endpoint['LastModifiedTimestamp'].replace(tzinfo=None)
                now_time = datetime.datetime.now()
                diff = now_time - created_timestamp
                created_minutes = diff.total_seconds()/60
                print('EndPoint Name : ' + endpoint_name,   'EndPoint AvailabilityZone : ' + endpoint_az,
                        'EndPointCreated : ' + str(created_timestamp),
                        'EndPointLastModifid : ' + str(lastmodified_timestamp),
                        'Endpoint Life Duration In Minutes : ' + str(created_minutes), sep='\n')
                if created_minutes > 120 :
                    msg = 'EndPoint Name : ' + endpoint_name + '\n' + 'Endpoint Alive Duration In Minutes : ' + str(created_minutes)
                    sub = "Alert - Glue Dev Endpoint Alive for more than 2 Hours"
                    publish_to_sns(sub, msg)
                

def publish_to_sns(sub, msg):
    topic_arn = "arn:aws:sns:us-west-1:338612595803:GlueDevEndpointEmailTopic"
    sns = boto3.client("sns")
    
    response = sns.publish(
        TopicArn=topic_arn,
        Message=msg,
        Subject=sub
    )
