import boto3

# Reference https://boto3.amazonaws.com/v1/documentation/api/1.9.42/reference/services/glue.html

glue_job_name = 'TestGlueCreate'
script_location = 's3://dev-driscolls-datalake-config/jobs/lci/initial/job_lci_bin_grower_exception_raw_to_transform.py'
command_name = 'glue_script'
region='us-west-1'
def_args = {
         'env': 'DEV',
		 'key1': '121',
		 'key2': '122'
     },
max_capacity = 2

#this is to track who is the owner/user/updater of the job being created 
tags = {'CreatedBy': 'Ashutosh',
		'CreatedByEmail': 'ashu.beginner@gmail.com',
		'UsedBy': 'Ashutosh',
		'UsedByEmail': 'ashu.beginner@gmail.com',
		'UpdatedBy': 'Ashutosh',
		'UpdatedByEmail': 'ashu.beginner@gmail.com',
		}

# global glue client
client = boto3.client('glue', region_name=region)


def create_glue_job():
	"""
	this is to create a new glue job
	"""
	try:
		response = client.create_job(
			 Name=name,
			 Description='this is to test glue job create',
			 Role='Glue-Service-Role',
			 ExecutionProperty={
				 'MaxConcurrentRuns': 123
			 },
			 Command={
				 'Name': command_name,
				 'ScriptLocation': script_location,
				 'PythonVersion': '3'
			 },
			 DefaultArguments=def_args,
			 MaxCapacity=max_capacity
			 Tags=tags,
			 GlueVersion='3.0',

	 )
	except Exception as e:
		raise e


def run_glue_job(job_name):
	"""
	this is to run any existing glue job.
	Valud Status : STARTING | RUNNING | STOPPING | STOPPED | SUCCEEDED | FAILED | TIMEOUT
	"""
	job_run_res = client.start_job_run(JobName=job_name)
	if job_run_res:
		run_id = job_run_res.get('JobRunId')
		status = get_job_status(job_name, run_id)
		print("Job Status - " + status)
	else:
		pass
	

def get_job_status(job_name, run_id):
	"""
	this is to get glue job status
	"""
	status = glue.get_job_run(JobName=job_name, RunId=run_id)
	return status['JobRun']['JobRunState']


def update_glue_job():
	"""
	this is to update any existing glue job
	"""
	try:
		response = client.update_job(JobName='TestGlueCreate',
						JobUpdate={'Role': 'Glue-Service-Role',
						'Command' :{'Name': 'glue_script',
									'ScriptLocation': 's3://dev-driscolls-datalake-config/jobs/lci/initial/job_lci_bin_grower_exception_raw_to_transform.py',
									'PythonVersion': '3'}, 
						'DefaultArguments': {'env': 'UAT'}})
	except Exception as e:
		raise e
