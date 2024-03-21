# AWS2
Lambda functions


import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    if event:
        print("Event : ", json.dumps(event))
        for record in event['Records']:
            action = record['eventName']
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            print(f"{action} detected on {bucket_name}/{object_key}")
    return 'Hello from Lambda'



YAML


AWSTemplateFormatVersion: '2010-09-09'
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: log-bucket-minibuild

  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Handler: index.lambda_handler
      Role: arn:aws:iam::339712850778:role/log-checker
      Code:
        S3Bucket: log-bucket-minibuild
        S3Key: log-lambda.py
      Runtime: python3.12

  LambdaInvokePermission:
    Type: AWS::Lambda::Permission
    Properties:
      Action: "lambda:InvokeFunction"
      FunctionName: !GetAtt LambdaFunction.Arn
      Principal: "s3.amazonaws.com"
      SourceArn: "arn:aws:s3:::log-bucket-minibuild"

  BucketNotification:
    Type: AWS::S3::BucketNotification
    Properties:
      Bucket: !Ref S3Bucket
      NotificationConfiguration:
        LambdaConfigurations:
          - Event: "s3:ObjectCreated:*"
            Function: !GetAtt LambdaFunction.Arn
          - Event: "s3:ObjectRemoved:*"
            Function: !GetAtt LambdaFunction.Arn
