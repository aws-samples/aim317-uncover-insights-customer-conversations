import boto3
import uuid
import json
import os

def lambda_handler(event, context):

    record = event['Records'][0]
    
    print("Record: " + str(record))
    
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    s3fileName = record['s3']['object']['key'].split("/")[-1]
    
    s3Path = "s3://" + s3bucket + "/" + s3object
    jobName = s3fileName + '-' + str(uuid.uuid4())

    client = boto3.client('transcribe')

    vocabLanguage = s3object.split('-')[3].split('.')[0]
    if vocabLanguage == "EN":
        vocabLanguage = 'en-US'
        vocabularyName = os.environ['ENVocabularyName']
    elif vocabLanguage == "ES":
        vocabLanguage = 'es-US'
        vocabularyName = os.environ['ESVocabularyName']
    
    response = client.start_transcription_job(
        TranscriptionJobName=jobName,
        LanguageCode=vocabLanguage,
        Settings = {'VocabularyName': vocabularyName,
                    'ShowSpeakerLabels': True,
                    'MaxSpeakerLabels': 2},
        Media={
            'MediaFileUri': s3Path
        },
        OutputBucketName = os.environ['outputBucket'],
        OutputKey = os.environ['outputKey'] + s3fileName.split(".")[0] + "-transcription"
        )

    return {
        'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName']
    }