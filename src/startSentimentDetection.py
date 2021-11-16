import awswrangler as wr
import pandas as pd
import boto3
import os

def lambda_handler(event, context):

    client = boto3.client('comprehend')

    inprefix = 'comprehendInput'
    outprefix = 'quicksight/temp/insights'

    comprehend = boto3.client('comprehend')
    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=os.environ['ComprehendBucket'], Prefix=inprefix)
    job_name_list = []
    t_prefix = 'quicksight/data/sentiment'

    cols = ['transcript_name', 'sentiment']
    df_sent = pd.DataFrame(columns=cols)

    for page in pages:
        for obj in page['Contents']:
            transcript_file_name = obj['Key'].split('/')[1]
            temp = s3_resource.Object(os.environ['ComprehendBucket'], obj['Key'])
            transcript_contents = temp.get()['Body'].read().decode('utf-8')
            response = comprehend.detect_sentiment(Text=transcript_contents, LanguageCode='en')
            df_sent.loc[len(df_sent.index)] = [transcript_file_name.strip('en-').strip('.txt'),response['Sentiment']]
            
    wr.s3.to_csv(df_sent, path='s3://' + os.environ['ComprehendBucket'] + '/' + t_prefix + '/' + 'sentiment.csv')
