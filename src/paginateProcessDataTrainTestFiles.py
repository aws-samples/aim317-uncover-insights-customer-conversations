import boto3
import os
import pandas as pd

def lambda_handler(event, context):

    raw_data = pd.read_csv('aim317-cust-class-train-data.csv')
    raw_data['label'] = raw_data['label'].astype(str)
    selected_columns = ['label', 'text']
    selected_data = raw_data[selected_columns]

    DSTTRAINFILE='comprehend-train.csv'

    selected_data.to_csv(path_or_buf=DSTTRAINFILE,
                    header=False,
                    index=False,
                    escapechar='\\',
                    doublequote=False,
                    quotechar='"')

    s3 = boto3.client('s3')
    prefix = 'comprehend-custom-classifier'
    bucket = os.environ['comprehendBucket']

    s3.upload_file(DSTTRAINFILE, bucket, prefix+'/' + DSTTRAINFILE)
    s3_train_data = 's3://{}/{}/{}'.format(bucket, prefix, DSTTRAINFILE)
    s3_output_job = 's3://{}/{}/{}'.format(bucket, prefix, 'output/train_job')
    print('training data location: ',s3_train_data, "output location:", s3_output_job)