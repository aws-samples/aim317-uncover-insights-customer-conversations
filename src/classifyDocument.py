import awswrangler as wr
import pandas as pd
import boto3
import os


def lambda_handler(event, context):

    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    comprehend = boto3.client('comprehend')
    t_prefix = 'quicksight/data/cta'

    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=os.environ['classifierBucket'], Prefix='comprehendInput')
    a = []

    cols = ['transcript_name', 'cta_status']
    df_class = pd.DataFrame(columns=cols)

    comprehendEndpoint = comprehend.list_endpoints(
        Filter={
            'Status': 'IN_SERVICE',
        }
    )

    for item in comprehendEndpoint.get('EndpointPropertiesList'):
        if 'document-classifier-endpoint' in item['EndpointArn']:
            endpointArn = item['EndpointArn']

    for page in pages:
        for obj in page['Contents']:
            transcript_file_name = obj['Key'].split('/')[1]
            temp = s3_resource.Object(os.environ['classifierBucket'], obj['Key'])
            transcript_content = temp.get()['Body'].read().decode('utf-8')
            transcript_truncated = transcript_content[-400:]
            response = comprehend.classify_document(Text=transcript_truncated, EndpointArn=endpointArn)
            a = response['Classes']
            tempcols = ['Name', 'Score']
            df_temp = pd.DataFrame(columns=tempcols)
            for i in range(0, 2):
                df_temp.loc[len(df_temp.index)] = [a[i]['Name'], a[i]['Score']]
            cta = df_temp.iloc[df_temp.Score.argmax(), 0:2]['Name']
            df_class.loc[len(df_class.index)] = [transcript_file_name.strip('en-').strip('.txt'), cta]        

    wr.s3.to_csv(df_class, path='s3://' + os.environ['classifierBucket'] + '/' + t_prefix + '/' + 'cta_status.csv')
