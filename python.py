import json
import boto3

def lambda_handler(event, context):
    # Initialize CloudWatch Logs client
    logs_client = boto3.client('logs')

    # Define the log group and stream
    log_group_name = 'S3BucketActivity'
    log_stream_name = 'UploadsAndDeletions'

    # Check if the log group exists, if not, create it
    log_groups = logs_client.describe_log_groups(logGroupNamePrefix=log_group_name)
    if not any(group['logGroupName'] == log_group_name for group in log_groups['logGroups']):
        logs_client.create_log_group(logGroupName=log_group_name)

    # Check if the log stream exists, if not, create it
    log_streams = logs_client.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
    if not any(stream['logStreamName'] == log_stream_name for stream in log_streams['logStreams']):
        logs_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)

    # Log the S3 event
    for record in event['Records']:
        # Construct the log message
        log_message = {
            'eventTime': record['eventTime'],
            'eventName': record['eventName'],
            'bucketName': record['s3']['bucket']['name'],
            'objectKey': record['s3']['object']['key']
        }

        # Put the log event
        logs_client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': int(record['eventTime']),
                    'message': json.dumps(log_message)
                },
            ],
        )

    return 'Successfully logged S3 event to CloudWatch'
