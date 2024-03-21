# AWS2
Lambda functions

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




{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Resources": {
    "MyS3Bucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": "log-bucket-minibuild"
      }
    },
    "MyLambdaFunction": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Handler": "log-lambda.lambda_handler",
        "Role": "arn:aws:iam::[your-account-id]:role/[your-lambda-role]",
        "Code": {
          "S3Bucket": "[your-lambda-code-bucket]",
          "S3Key": "log-lambda.zip"
        },
        "Runtime": "python3.8",
        "Timeout": 30
      }
    },
    "MyLambdaInvokePermission": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "MyLambdaFunction",
            "Arn"
          ]
        },
        "Principal": "s3.amazonaws.com",
        "SourceArn": {
          "Fn::GetAtt": [
            "MyS3Bucket",
            "Arn"
          ]
        }
      }
    },
    "MyBucketNotification": {
      "Type": "AWS::S3::BucketNotification",
      "Properties": {
        "Bucket": {
          "Ref": "MyS3Bucket"
        },
        "NotificationConfiguration": {
          "LambdaConfigurations": [
            {
              "Event": "s3:ObjectCreated:*",
              "Function": {
                "Fn::GetAtt": [
                  "MyLambdaFunction",
                  "Arn"
                ]
              }
            },
            {
              "Event": "s3:ObjectRemoved:*",
              "Function": {
                "Fn::GetAtt": [
                  "MyLambdaFunction",
                  "Arn"
                ]
              }
            }
          ]
        }
      }
    }
  }
}








