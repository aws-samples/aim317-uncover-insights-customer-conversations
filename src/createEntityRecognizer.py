import boto3
import uuid
import os

def lambda_handler(event, context):

    record = event['Records'][0]
       
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    
    jobName = "aim317-recognizer" + '-' + str(uuid.uuid4())

    client = boto3.client('comprehend')

    s3TrainingBucket = os.environ['ComprehendTrainBucket']
    s3AnnotationBucket = os.environ['ComprehendAnnotationBucket']

    response = client.create_entity_recognizer(
        RecognizerName=jobName,
        DataAccessRoleArn=os.environ['ComprehendARN'],
        InputDataConfig={
            'DataFormat': 'COMPREHEND_CSV',
            "EntityTypes": [
                    {
                        "Type": "MOVEMENT"
                    },
                    {
                        "Type": "BRAIN"
                    },
                    {
                        "Type": "ETHICS"
                    }
                ],
            'Documents': {
                'S3Uri': "s3://" + s3TrainingBucket + "/comprehend/train/train_ds.csv",
                'InputFormat': 'ONE_DOC_PER_LINE'
            },
            'Annotations': {
                'S3Uri': "s3://" + s3AnnotationBucket + "/comprehend/train/annotation.csv",
            }
        },
        LanguageCode='en',
        VersionName= 'v001'
    )

    return {
        'EntityRecognizerArn': response['EntityRecognizerArn']
    }