import boto3
import os
import pandas as pd
import subprocess
import json
import time
import pprint
import numpy as np
import string
import datetime 
import random

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    bucket = os.environ['s3Bucket']
    prefix = 'Comprehend-Custom-Classification'
    bucket = 'aim317-workshop-bucket'

    DSTTRAINFILE='data/training/comprehend-train.csv'
    DSTVALIDATIONFILE='data/test/comprehend-test.csv'

    raw_data = pd.read_csv('data/training/aim317-cust-class-train-data.csv')
    raw_data['label'] = raw_data['label'].astype(str)
    raw_data.groupby('label')['text'].count()
    selected_columns = ['label', 'text']
    selected_data = raw_data[selected_columns]
    selected_data.shape
    selected_data.groupby('label')['text'].count()

    selected_data.to_csv(path_or_buf=DSTTRAINFILE,
                    header=False,
                    index=False,
                    escapechar='\\',
                    doublequote=False,
                    quotechar='"')

    s3 = boto3.client('s3')
    comprehend = boto3.client('comprehend')

    s3.upload_file(DSTTRAINFILE, bucket, prefix+'/'+DSTTRAINFILE)

    s3_train_data = 's3://{}/{}/{}'.format(bucket, prefix, DSTTRAINFILE)
    s3_output_job = 's3://{}/{}/{}'.format(bucket, prefix, 'output/train_job')
    print('training data location: ',s3_train_data, "output location:", s3_output_job)

    id = str(datetime.datetime.now().strftime("%s"))
    training_job = comprehend.create_document_classifier(
        DocumentClassifierName='BYOD-Custom-Classifier-'+ id,
        DataAccessRoleArn=os.environ['ServiceRoleArn'],
        InputDataConfig={
            'S3Uri': s3_train_data
        },
        OutputDataConfig={
            'S3Uri': s3_output_job
        },
        LanguageCode='en',
        VersionName= 'v001',
    )

    response = comprehend.describe_document_classifier(
        DocumentClassifierArn=training_job['DocumentClassifierArn']
    )
