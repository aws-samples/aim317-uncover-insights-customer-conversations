import boto3
import uuid
import os

def lambda_handler(event, context):

    record = event['Records'][0]
       
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    
    s3Path = "s3://" + s3bucket + "/" + s3object
    jobName = s3object.replace("/","_") + '-' + str(uuid.uuid4())

    client = boto3.client('comprehend')

    ## Start Sentiment Detection Job
    response = client.start_sentiment_detection_job(
    
    InputDataConfig={
        'S3Uri': s3Path,
        'InputFormat': 'ONE_DOC_PER_FILE',
        'DocumentReaderConfig': {
            'DocumentReadAction': 'TEXTRACT_ANALYZE_DOCUMENT',
        }
    },
    OutputDataConfig={
        'S3Uri': os.environ['ComprehendTargetBucket']
    },
    DataAccessRoleArn=os.environ['ComprehendARN'],
    JobName=jobName,
    LanguageCode='en'
    
    )