import json
import boto3
import io
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

def lambda_handler(event, context):

    bucket = event["bucket"]
    file = event["file"]

    logger.info('Starting Analyzing Image');
    logger.info('Bucket: %s', bucket);
    logger.info('File: %s', file);

    description = "";

    # Invoke Rekognition service
    celebrities = rekognition.recognize_celebrities(Image={ 'S3Object': { 'Bucket': bucket, 'Name': file } })["CelebrityFaces"]

    if len(celebrities) == 0:
        description = "I don't see anybody famous in the picture!"

    if len(celebrities) > 0:
        names = []
        for celebrity in celebrities:
            names.append(celebrity["Name"])

        description = "I see " + ', '.join(names) + " on the picture!";

    logger.info('Description: %s', description);


    #Preparing local file with description
    txtName = file[:-4] + ".txt"
    f = open('/tmp/' + txtName, "w")
    f.write(description)
    f.close();

    #Copying file back to S3
    s3.upload_file('/tmp/' + txtName, bucket, txtName)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
