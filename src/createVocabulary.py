import boto3
import uuid
import json
import os

def lambda_handler(event, context):

    record = event['Records'][0]
            
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    
    print(s3object.split(".")[0].split("-")[2])

    if s3object.split(".")[0].split("-")[2] == "EN":
    
        s3Path = "s3://" + s3bucket + "/" + s3object
        VocabName = "custom-vocab-EN-" + str(uuid.uuid4())

        client = boto3.client('transcribe')

        print("S3 Path:" + s3Path)

        response = client.create_vocabulary(
            VocabularyName=VocabName,
            LanguageCode='en-US',
            VocabularyFileUri = s3Path,
        )

        return {
            'VocabularybName': response['VocabularyName']
        }
    
    elif s3object.split(".")[0].split("-")[2] == "ES":
        s3Path = "s3://" + s3bucket + "/" + s3object
        VocabName = "custom-vocab-ES-" + str(uuid.uuid4())

        client = boto3.client('transcribe')

        print("S3 Path:" + s3Path)

        response = client.create_vocabulary(
            VocabularyName=VocabName,
            LanguageCode='es-ES',
            VocabularyFileUri = s3Path,
        )

        return {
            'VocabularybName': response['VocabularyName']
        }
    
    else:
        
        return {
            'ErrorCode': "Language not in filename, must end in EN or ES"
        }