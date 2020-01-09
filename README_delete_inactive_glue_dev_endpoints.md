>> 

##### create glue client for each region and get all dev endpoints
#
```
import boto3
client = boto3.client('glue', region_name='us-west-2')
endpoint_res = client.get_dev_endpoints()
```
##### here is how endpoint response looks like
#
```sh
>>endpoint_res
		{
			u 'NextToken': u '', u 'DevEndpoints': [{
				u 'Status': u 'READY',
				u 'AvailabilityZone': u 'us-west-1c',
				u 'PublicAddress': u 'ec2-13-57-33-86.us-west-1.compute.amazonaws.com',
				u 'RoleArn': u 'arn:aws:iam::XX:role/GlueExecutionRole',
				u 'GlueVersion': u '1.0',
				u 'ZeppelinRemoteSparkInterpreterPort': 9007,
				u 'CreatedTimestamp': datetime.datetime(2020, 1, 9, 10, 28, 58, 148000, tzinfo = tzlocal()),
				u 'EndpointName': u 'AshuTest',
				u 'ExtraPythonLibsS3Path': u 's3://ashu-glue-bucket',
				u 'SecurityGroupIds': [],
				u 'LastModifiedTimestamp': datetime.datetime(2020, 1, 9, 10, 34, 52, 768000, tzinfo = tzlocal()),
				u 'NumberOfNodes': 2,
				u 'Arguments': {
					u '--enable-glue-datacatalog': u ' ',
					u 'GLUE_PYTHON_VERSION': u '3'
				}
			}], 'ResponseMetadata': {
				'RetryAttempts': 0,
				'HTTPStatusCode': 200,
				'RequestId': 'ac0a6cf1-329d-11ea-b6d8-8dcfe84008f0',
				'HTTPHeaders': {
					'date': 'Thu, 09 Jan 2020 05:05:36 GMT',
					'x-amzn-requestid': 'ac0a6cf1-329d-11ea-b6d8-8dcfe84008f0',
					'content-length': '536',
					'content-type': 'application/x-amz-json-1.1',
					'connection': 'keep-alive'
				}
			}
		}
```
##### Get the created timestamp for the endpoint
#
```
created_timestamp = endpoint_res['DevEndpoint']['CreatedTimestamp']
```

##### Now create cloudtrail client 
#
```
ct_conn = boto3.client(service_name='cloudtrail',region_name='us-west-1')
starttime = datetime.datetime.now() - datetime.timedelta(days=1)
endtime = datetime.datetime.now()
```
##### get the events withi given timeframe say 1 day
#
```
res = ct_conn.lookup_events(StartTime=starttime, EndTime=endtime, MaxResults=50)
```
##### Here is how event response looks like
#
```sh
		{
			u 'NextToken': u 'skl7ZActhq7ZudqmzJf0OEkSt7qJo8O+GJSVQDiWuvFpKUigAUnpvOCSeHDUiaIaDXXuhdJw8M1OBP2zeislTg==', u 'Events': [{
					u 'EventId': u 'b91c9ab7-f980-4e5e-a590-9e625b27517c',
					u 'Username': u 'root',
					u 'EventTime': datetime.datetime(2020, 1, 9, 11, 7, 9, tzinfo = tzlocal()),
					u 'CloudTrailEvent': u '{"eventVersion":"1.05","userIdentity":{"type":"Root","principalId":"338612595803","arn":"arn:aws:iam::xx:root","accountId":"xx","accessKeyId":"xx","sessionContext":{"attributes":{"mfaAuthenticated":"false","creationDate":"2020-01-09T04:56:44Z"}},"invokedBy":"signin.amazonaws.com"},"eventTime":"2020-01-09T05:37:09Z","eventSource":"glue.amazonaws.com","eventName":"GetTags","awsRegion":"us-west-1","sourceIPAddress":"165.225.104.109","userAgent":"signin.amazonaws.com","requestParameters":{"resourceArn":"arn:aws:glue:us-west-1:xx:devEndpoint/AshuTest"},"responseElements":{"tags":{"Name":"TestDevEndPoint"}},"requestID":"141babfa-32a2-11ea-b6d8-8dcfe84008f0","eventID":"b91c9ab7-f980-4e5e-a590-9e625b27517c","eventType":"AwsApiCall","recipientAccountId":"xx"}',
					u 'AccessKeyId': u 'ASIAU5VXCFRNSTBWEMV5',
					u 'EventName': u 'GetTags',
					u 'ReadOnly': u 'true',
					u 'EventSource': u 'glue.amazonaws.com',
					u 'Resources': []
				}, {
					u 'EventId': u 'dae9c213-528a-47ea-8a1d-c5f952d09937',
					u 'Username': u 'root',
					u 'EventTime': datetime.datetime(2020, 1, 9, 11, 7, 6, tzinfo = tzlocal()),
					u 'CloudTrailEvent': u '{"eventVersion":"1.05","userIdentity":{"type":"Root","principalId":"xx","arn":"arn:aws:iam::xx:root","accountId":"xx","accessKeyId":"xx","sessionContext":{"sessionIssuer":{},"webIdFederationData":{},"attributes":{"mfaAuthenticated":"false","creationDate":"2020-01-09T04:56:44Z"}},"invokedBy":"glue.amazonaws.com"},"eventTime":"2020-01-09T05:37:06Z","eventSource":"tagging.amazonaws.com","eventName":"GetResources","awsRegion":"us-west-1","sourceIPAddress":"glue.amazonaws.com","userAgent":"glue.amazonaws.com","requestParameters":{"tagFilters":[],"resourcesPerPage":50,"resourceTypeFilters":["glue:devEndpoint"]},"responseElements":null,"requestID":"3dbce1cc-b205-4769-bf24-0fc4ecd22741","eventID":"dae9c213-528a-47ea-8a1d-c5f952d09937","readOnly":true,"eventType":"AwsApiCall","recipientAccountId":"xx"}',
					u 'AccessKeyId': u 'xx',
					u 'EventName': u 'GetResources',
					u 'ReadOnly': u 'true',
					u 'EventSource': u 'tagging.amazonaws.com',
					u 'Resources': []
				}, {
					u 'EventId': u '555bed03-ae3c-4a07-b02c-81e6bc3cab17',
					u 'Username': u 'root',
					u 'EventTime': datetime.datetime(2020, 1, 9, 11, 6, 48, tzinfo = tzlocal()),
					u 'CloudTrailEvent': u '{"eventVersion":"1.05","userIdentity":{"type":"Root","principalId":"xx","arn":"arn:aws:iam::xx:root","accountId":"xx","accessKeyId":"xx","sessionContext":{"sessionIssuer":{},"webIdFederationData":{},"attributes":{"mfaAuthenticated":"false","creationDate":"2020-01-09T04:56:44Z"}},"invokedBy":"signin.amazonaws.com"},"eventTime":"2020-01-09T05:36:48Z","eventSource":"ec2.amazonaws.com","eventName":"DescribeInstances","awsRegion":"us-west-1","sourceIPAddress":"165.225.104.109","userAgent":"signin.amazonaws.com","requestParameters":{"instancesSet":{},"filterSet":{"items":[{"name":"tag-key","valueSet":{"items":[{"value":"aws-glue-dev-endpoint"}]}},{"name":"tag-value","valueSet":{"items":[{"value":"AshuTest"}]}}]}},"responseElements":null,"requestID":"83543c2b-e0ed-4083-a3f1-ea70907fa339","eventID":"555bed03-ae3c-4a07-b02c-81e6bc3cab17","eventType":"AwsApiCall","recipientAccountId":"xx"}',
					u 'AccessKeyId': u 'xx',
					u 'EventName': u 'DescribeInstances',
					u 'ReadOnly': u 'true',
					u 'EventSource': u 'ec2.amazonaws.com',
					u 'Resources': []
				}
			}
```
> Now for every glue dev endpoint check if there is any event in the cloudtrail resultset ,
> if no activity found we can notify the DL or we can delete the endpoint
```        
response = client.delete_dev_endpoint(EndpointName='AshuTest')
```
