import boto3
import json

client = boto3.client('lambda')

function_name = "DaysCounter"

lambda_payload = {"year":"1987","month":"2","day":"3"}

for x in range(1000):
    response = client.invoke(
        FunctionName='DaysCounter',
        InvocationType='RequestResponse',
        Payload=json.dumps(lambda_payload)
    )

print(json.loads(response['Payload'].read()))
