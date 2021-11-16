import boto3
import json
import os

def lambda_handler(event, context):

    record = event['Records'][0]
       
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']

    s3 = boto3.client('s3')
    s3Resource = boto3.resource('s3')
    transcribe = boto3.client('transcribe')
    translate = boto3.client('translate')

    ## Get the transcription job name from the filename that triggered the event

    response = transcribe.list_transcription_jobs(
        JobNameContains='-'.join(s3object.split("/")[1].split("-")[0:3])
    )

    TranscriptionJobName = response['TranscriptionJobSummaries'][0]['TranscriptionJobName']

    transcribed_data = s3Resource.Object(s3bucket,s3object)
    original = json.loads(transcribed_data.get()['Body'].read().decode('utf-8'))
    entire_transcript = original['results']['transcripts']
    print(entire_transcript)
    outfile = '/tmp/'+ TranscriptionJobName +'.txt'
    with open(outfile, 'w') as out:
        out.write(entire_transcript[0]['transcript'])
    s3.upload_file(outfile,os.environ['outputBucket'], 'translateInput' + TranscriptionJobName +'.txt')

    ## Now get the language code from the transcription job

    response = transcribe.get_transcription_job(
        TranscriptionJobName=TranscriptionJobName
    )

    TranslateLanguageCode = response['TranscriptionJob']['LanguageCode'].split("-")[0]

    if TranslateLanguageCode != 'en':

        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=os.environ['outputBucket'], Prefix='translateInput' + TranscriptionJobName +'.txt')
        for page in pages:
            for obj in page['Contents']:
                temp = s3Resource.Object(s3bucket, obj['Key'])
                trans_input = temp.get()['Body'].read().decode('utf-8')
                if len(trans_input) > 0:
                    # Translate the Spanish transcripts
                    trans_response = translate.translate_text(
                        Text=trans_input,
                        TerminologyNames=['aim317-custom-terminology'],
                        SourceLanguageCode='es',
                        TargetLanguageCode='en'
                    )
                    # Write the translated text to a temporary file
                    with open('/tmp/temp_translate.txt',  'w') as outfile:
                        outfile.write(trans_response['TranslatedText'])
                    # Upload the translated text to S3 bucket
                    s3.upload_file('/tmp/temp_translate.txt', os.environ['outputBucket'], 'comprehendInput' + '/en-' + TranscriptionJobName)
                    print("Translated text file uploaded to: " + 's3://' + os.environ['outputBucket'] + '/' + 'comprehendInput' + '/en-' + TranscriptionJobName)
        
    else:

        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=os.environ['outputBucket'], Prefix='translateInput' + TranscriptionJobName +'.txt')
        for page in pages:
            for obj in page['Contents']:
                temp = s3Resource.Object(s3bucket, obj['Key'])
                file_input = temp.get()['Body'].read().decode('utf-8')
                with open('/tmp/temp_translate.txt',  'w') as outfile:
                    outfile.write(file_input)
                s3.upload_file('/tmp/temp_translate.txt', os.environ['outputBucket'], 'comprehendInput' + '/en-' + TranscriptionJobName)
                print("Translated text file uploaded to: " + 's3://' + os.environ['outputBucket'] + '/' + 'comprehendInput' + '/en-' + TranscriptionJobName)