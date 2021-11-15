import boto3

def lambda_handler(event, context):

    record = event['Records'][0]
    
    print("Record: " + str(record))
        
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']

    s3Path = "s3://" + s3bucket + "/" + s3object

    s3_resource = boto3.resource('s3')

    temp = s3_resource.Object(s3bucket, s3object)
    term_file = temp.get()['Body'].read().decode('utf-8')

    client = boto3.client('translate')

    print("S3 Path:" + s3Path)

    response = client.import_terminology(
        Name="aim317-custom-terminology",
        MergeStrategy='OVERWRITE',
        TerminologyData={
            'File': term_file,
            'Format': 'CSV'
        },
    )

    return {
        'TerminologyName': response['TerminologyProperties']['Name']
    }