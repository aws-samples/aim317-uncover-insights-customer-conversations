import boto3
import uuid
import os

def lambda_handler(event, context):

    record = event['Records'][0]
       
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    
    jobName = s3object.replace("/","_") + '-' + str(uuid.uuid4())

    ## Get the transcription job name from the filename that triggered the event
    client = boto3.client('transcribe')

    response = client.list_transcription_jobs(
        JobNameContains='-'.join(s3object.split("/")[1].split("-")[0:3])
    )

    TranscriptionJobName = response['TranscriptionJobSummaries'][0]['TranscriptionJobName']

    ## Now get the language code from the transcription job

    response = client.get_transcription_job(
        TranscriptionJobName=TranscriptionJobName
    )

    TranslateLanguageCode = response['TranscriptionJob']['LanguageCode'].split("-")[0]

    if TranslateLanguageCode != 'en':

        client = boto3.client('translate')

        response = client.start_text_translation_job(
            JobName="AIM317-Translate-" + s3object.split("/")[1],
            InputDataConfig={
                'S3Uri': "s3://" + s3bucket + "/" + s3object.split("/")[0],
                'ContentType': 'text/plain'
            },
            OutputDataConfig={
                'S3Uri': "s3://" + os.environ['outputBucket'] + "/" + os.environ['outputKey']
            },
            DataAccessRoleArn=os.environ['TranslateARN'],
            SourceLanguageCode=TranslateLanguageCode,
            TargetLanguageCodes=[
                'en',
            ],
            TerminologyNames=[
                'aim317-custom-terminology',
            ]
        )

        return {
            'TranslationJobID': response['JobId']
        }

    else:

        client = boto3.client('s3')

        copy_source = {
            'Bucket': s3bucket,
            'Key': s3object
        }
        client.meta.client.copy(copy_source, os.environ['outputBucket'], os.environ['outputKey'])