import boto3
import os
import io
import pandas as pd

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    raw_data = s3.get_object(Bucket=os.environ['comprehendBucket'], Key='comprehend/train/aim317-cust-class-train-data.csv')
    raw_content = pd.read_csv(io.BytesIO(raw_data['Body'].read()))
    print(raw_content)
    raw_content['label'] = raw_content['label'].astype(str)
    selected_columns = ['label', 'text']
    selected_data = raw_content[selected_columns]

    DSTTRAINFILE='/tmp/comprehend-train.csv'

    selected_data.to_csv(path_or_buf=DSTTRAINFILE,
                    header=False,
                    index=False,
                    escapechar='\\',
                    doublequote=False,
                    quotechar='"')

    s3 = boto3.client('s3')
    prefix = 'comprehend-custom-classifier'
    bucket = os.environ['comprehendBucket']

    s3.upload_file(DSTTRAINFILE, bucket, prefix+'/comprehend-train.csv')