import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambdaClient = boto3.client('lambda')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    file = event['Records'][0]['s3']['object']['key']

    logger.info('New File Detected!');
    logger.info('Bucket: %s', bucket);
    logger.info('File: %s', file);

    #Check if file is an image. If yes, analyze it!
    if ( file.endswith(".jpg") ):
        response = lambdaClient.invoke(
            FunctionName = 'AnalyzeImage',
            InvocationType = 'RequestResponse',
            Payload = json.dumps({ 'bucket' : bucket, 'file'  : file })
        )

    #Check if file is an text. If yes, analyze it!
    if ( file.endswith(".txt") ):
        response = lambdaClient.invoke(
            FunctionName = 'CreateAudio',
            InvocationType = 'RequestResponse',
            Payload = json.dumps({ 'bucket' : bucket, 'file'  : file })
        )


    return "OK";
