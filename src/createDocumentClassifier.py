import boto3
import uuid
import os

def lambda_handler(event, context):

    DSTTRAINFILE='comprehend-train.csv'
    
    s3_train_data = 's3://{}/{}/{}'.format(os.environ['classifierBucket'], os.environ['classifierBucketPrefix'], DSTTRAINFILE)
    s3_output_job = 's3://{}/{}/{}'.format(os.environ['classifierBucket'], os.environ['classifierBucket'], 'output/train_job')
    print('training data location: ',s3_train_data, "output location:", s3_output_job)

    uid = uuid.uuid4()
    comprehend = boto3.client('comprehend')

    training_job = comprehend.create_document_classifier(
        DocumentClassifierName='aim317-custom-classifier-' + uid,
        DataAccessRoleArn=os.environ['ComprehendARN'],
        InputDataConfig={
            'S3Uri': s3_train_data
        },
        OutputDataConfig={
            'S3Uri': s3_output_job
        },
        LanguageCode='en',
        VersionName='v001'
    )

    return {
        'DocumentClassifierArn': training_job['DocumentClassifierArn']
    }