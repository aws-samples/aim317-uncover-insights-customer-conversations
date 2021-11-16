import boto3
import os
import pandas as pd
import awswrangler as wr

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    comprehend = boto3.client('comprehend')

    t_prefix = 'quicksight/data/entity'

    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=os.environ['entityDetectionBucket'], Prefix='comprehendInput/')

    tempcols = ['Type', 'Score']
    df_temp = pd.DataFrame(columns=tempcols)

    cols = ['transcript_name', 'entity_type']
    df_ent = pd.DataFrame(columns=cols)

    comprehendEndpoint = comprehend.list_endpoints(
        Filter={
            'Status': 'IN_SERVICE',
        }
    )

    for item in comprehendEndpoint.get('EndpointPropertiesList'):
        if 'entity-recognizer-endpoint' in item['EndpointArn']:
            endpointArn = item['EndpointArn']

    for page in pages:
        for obj in page['Contents']:
            transcript_file_name = obj['Key'].split('/')[1]
            temp = s3_resource.Object(os.environ['entityDetectionBucket'], obj['Key'])
            transcript_content = temp.get()['Body'].read().decode('utf-8')
            transcript_truncated = transcript_content[500:1800]
            response = comprehend.detect_entities(Text=transcript_truncated, LanguageCode='en', EndpointArn=endpointArn)
            df_temp = pd.DataFrame(columns=tempcols)
            for ent in response['Entities']:
                df_temp.loc[len(df_temp.index)] = [ent['Type'],ent['Score']]
            if len(df_temp) > 0:
                entity = df_temp.iloc[df_temp.Score.argmax(), 0:2]['Type']
            else:
                entity = 'No entities'
            
            df_ent.loc[len(df_ent.index)] = [transcript_file_name.strip('en-'),entity]        

    wr.s3.to_csv(df_ent, path='s3://' + os.environ['entityDetectionBucket'] + '/' + t_prefix + '/' + 'entities.csv')
