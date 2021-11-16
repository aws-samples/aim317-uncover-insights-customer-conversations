import boto3
import uuid
import os

def lambda_handler(event, context):

    ## Get Model ARN depending on argument passed

    client = boto3.client('comprehend')

    requestParams = event['endpointType']
    
    if requestParams == "EntityRecognizer":
        endpointName = "aim317-entity-recognizer" + '-' + str(uuid.uuid4())[:8]
        response = client.list_entity_recognizers(
            Filter={
                'Status': 'TRAINED',
            }
        )
        if not response['EntityRecognizerPropertiesList']:
            return "No models trained, please check the Comprehend dashboard"

        modelARN = response['EntityRecognizerPropertiesList'][0]['EntityRecognizerArn']

    elif requestParams == "DocumentClassifier":
        endpointName = "aim317-document-classifier" + '-' + str(uuid.uuid4())[:8]

        response = client.list_document_classifiers(
            Filter={
                'Status': 'TRAINED',
            }
        )
        if not response['DocumentClassifierPropertiesList']:
            return "No models trained, please check the Comprehend dashboard"
        
        modelARN = response['DocumentClassifierPropertiesList'][0]['DocumentClassifierArn']

    response = client.create_endpoint(
        EndpointName=endpointName,
        ModelArn=modelARN,
        DesiredInferenceUnits=4,
        DataAccessRoleArn=os.environ['ComprehendARN']
    )

    return {
        'EndpointArn': response['EndpointArn']
    }