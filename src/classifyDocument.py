import boto3
import os
import pandas as pd

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    comprehend = boto3.client('comprehend')
    runtime_region = os.environ['AWS_REGION']
    accountID = context.invoked_function_arn.split(":")[4]
    t_prefix = 'quicksight/data/cta'

    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=os.environ['classifierBucket'], Prefix='comprehend/input')
    a = []

    cols = ['transcript_name', 'cta_status']
    df_class = pd.DataFrame(columns=cols)

    comprehendEndpoint = comprehend.list_endpoints(
        Filter={
            'ModelArn': 'arn:aws:comprehend:runtime_region:accountID:entity-recognizer-endpoint/aim317-entity-recognizer-760259c4',
            'Status': 'IN_SERVICE',
        }
    )

    for page in pages:
        for obj in page['Contents']:
            cta = ''
            transcript_file_name = obj['Key'].split('/')[2]
            temp = s3_resource.Object(os.environ['classifierBucket'], obj['Key'])
            transcript_content = temp.get()['Body'].read().decode('utf-8')
            transcript_truncated = transcript_content[-400:]
            response = comprehend.classify_document(Text=transcript_truncated, EndpointArn=comprehendEndpoint['EndpointPropertiesList'][0]['EndpointArn'])
            a = response['Classes']
            tempcols = ['Name', 'Score']
            df_temp = pd.DataFrame(columns=tempcols)
            for i in range(0, 2):
                df_temp.loc[len(df_temp.index)] = [a[i]['Name'], a[i]['Score']]
            cta = df_temp.iloc[df_temp.Score.argmax(), 0:2]['Name']
            df_class.loc[len(df_class.index)] = [transcript_file_name.strip('en-').strip('.txt'), cta]        

    df_class.to_csv('s3://' + os.environ['classifierBucket'] + '/' + os.environ['classifierBucketPrefix'] + '/' + 'cta_status.csv', index=False)
    df_class