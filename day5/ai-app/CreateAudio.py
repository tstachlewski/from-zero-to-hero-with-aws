import json
import boto3
import io
import logging
import os
from contextlib import closing

logger = logging.getLogger()
logger.setLevel(logging.INFO)

comprehend = boto3.client('comprehend')
polly = boto3.client('polly')
s3 = boto3.client('s3')

languages = {'pl':'Maja','en':'Matthew','de':'Vicki','fr':'Celine','ja':'Mizuki'}


def lambda_handler(event, context):

    bucket = event["bucket"]
    file = event["file"]

    logger.info('Creating Audio file based on text');
    logger.info('Bucket: %s', bucket);
    logger.info('File: %s', file);

    # Saving file in local directory
    s3 = boto3.resource('s3')
    s3.meta.client.download_file(bucket, file, "/tmp/"+file)

    # Reading a file
    with open("/tmp/"+file, 'r') as myfile:
        content=myfile.read().replace('\n', '')

    logger.info('Content:');
    logger.info(content);

    # Detect language
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_dominant_language(
        Text=content
    )
    language = response['Languages'][0]['LanguageCode']
    voice =  languages[language]

    logger.info('Language: %s', language);
    logger.info('Voice: %s', voice);

    # Using Amazon Polly service to convert text to speech
    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=content,
        TextType='text',
        VoiceId=voice
    )

    # Save audio on local directory
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join("/tmp/", file)
            with open(output, "wb") as audioFile:
                audioFile.write(stream.read())

    # Save audio file on S3
    newName = file[:-4] + ".mp3"
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/' + file, bucket, newName)
    s3.put_object_acl(ACL='public-read', Bucket=bucket, Key = newName)

    #Creating new record in DynamoDB table
    location = s3.get_bucket_location(Bucket=bucket)
    region = location['LocationConstraint']
    url_begining = "https://s3-" + str(region) + ".amazonaws.com/"
    url = url_begining + bucket + "/" + newName


    logger.info('URL: %s', url);

    #Adding information about new audio file to DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("Interactions")
    table.put_item(
        Item={
            'name' : file[:-4],
            'text' : content,
            'language' : language,
            'voice' : voice,
            'url' : url
        }
    )

    return "OK"
