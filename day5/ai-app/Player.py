import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
import json

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):



    if "queryStringParameters" in event:
        if "name" in event["queryStringParameters"]:

            name = event["queryStringParameters"]["name"]

            table = dynamodb.Table("Interactions")

            items = table.query(KeyConditionExpression=Key('name').eq(name))

            url = items['Items'][0]['url']

            response = {
                    'statusCode': "200",
                    'body': " \
                        <html> \
                            <div style='text-align: center'> \
                                <br/><br/><br/><br/><br/><br/><br/><br/>\
                                <img src='https://s3.amazonaws.com/www.awspolska.pl/ext/awslogo.png' width=250><br/><br/><br/><br/> \
                            <body bgcolor='#e6eeff'> \
                                <audio controls><source src='" + url + "' type='audio/mp3'></audio> \
                            </body> \
                            </div> \
                        </html>",
                    'headers': {
                        'Content-Type': 'text/html',
                    }
                }
        else:
            response = { 'statusCode': "200", 'body': "NO PARAMETER!", 'headers': { 'Content-Type': 'text/html', } }
    else:
        response = { 'statusCode': "200", 'body': "NO PARAMETER!", 'headers': { 'Content-Type': 'text/html', } }

    return response
