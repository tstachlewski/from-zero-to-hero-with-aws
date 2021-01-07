import json
import boto3
import logging
import base64
import urllib.request
import io
import uuid
import time
from boto3.dynamodb.conditions import Key, Attr


logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambdaClient = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sns = boto3.client('sns')
connect = boto3.client('connect')

def lambda_handler(event, context):

    payload = json.loads(json.dumps(event['body']))
    payload = json.loads(base64.b64decode(payload).decode())

    text = payload["text"]
    image = payload["image"]
    phone = '+48' + payload["phone"]
    type = payload["type"]
    email = payload["email"]

    logger.info('Params');
    logger.info('Text: %s', text);
    logger.info('Image: %s', image);
    logger.info('Phone Number: %s', phone);
    logger.info('Type: %s', type);
    logger.info('Email: %s', email);

    file_id = str(uuid.uuid4());

    if image:
        downloadImageToS3(file_id, image)
    else:
        createTextFile(file_id, text);


    #Wait until result will be in DynamoDB
    table = dynamodb.Table("Interactions")
    while True:
        items = table.query(KeyConditionExpression=Key('name').eq(file_id))
        if len(items['Items']) > 0:
            url = items['Items'][0]['url']
            language = items['Items'][0]['language']
            text = items['Items'][0]['text']
            break;
        else:
            time.sleep(0.5)


    if type == 2:
        logger.info('Sending SMS: %s', url);
        sns.publish( PhoneNumber=phone, Message = url );

    if type == 3:
        callUser(language, text, phone)



    if email:
        table = dynamodb.Table("Contacts")
        table.put_item(
            Item={
                'email' : email
            }
        )


    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
            },
        'body': url
    };

def createTextFile(file_id, text):
    file = file_id + ".txt";
    f = open('/tmp/' + file, "w")
    f.write(text)
    f.close()
    s3.upload_file('/tmp/' + file, "a-test-bucket-tomek-1", file)

def downloadImageToS3(file_id, image):
    file = file_id + ".jpg";
    urllib.request.urlretrieve(image, '/tmp/' + file)
    s3.upload_file('/tmp/' + file, "a-test-bucket-tomek-1", file)


def callUser(language, text, phone):

    instanceId = '9ebe3d3d-e53c-4167-8764-582e82c68450'
    sourcePhoneNumber = '+48800088030'

    if language == 'pl':
        contactFlowId = 'b30ac8f2-9679-4b42-bd58-dc9ff3f08c48'

    if language == 'en':
        contactFlowId = '23b715cf-2c9f-453b-b521-1c7cb5e4cb2f'

    if language == 'de':
        contactFlowId = '3494e68b-fc90-4baf-bd62-8e925217204e'

    if language == 'fr':
        contactFlowId = 'db8307a3-9e9b-428c-9d59-5f3784358dfe'

    logger.info('Calling!');
    logger.info('Phone Number: %s ...', phone[0:9]);
    logger.info('Text: %s', text);
    logger.info('Language: %s', language);
    logger.info('Contact Flow ID: %s', contactFlowId);

    connect.start_outbound_voice_contact(
        DestinationPhoneNumber=phone,
        ContactFlowId=contactFlowId,
        InstanceId=instanceId,
        SourcePhoneNumber=sourcePhoneNumber,
        Attributes={
            'text': text
        }
    )
