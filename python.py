
import json
import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    # Log the event
    logger.info(f"Event: {json.dumps(event)}")
    
    # Iterate over each record
    for record in event['Records']:
        # Get the bucket name and key for the uploaded/deleted object
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        # Perform your processing here (e.g., read the object, log additional details)
        # For example, to get the object and print its contents:
        if 'ObjectCreated' in record['eventName']:
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            object_content = response['Body'].read()
            logger.info(f"Object content: {object_content}")
        
        # Log the event type (upload/deletion) and the object details
        logger.info(f"{record['eventName']} event detected for object {object_key} in bucket {bucket_name}")

    return {
        'statusCode': 200,
        'body': json.dumps('Event processed.')
    }
