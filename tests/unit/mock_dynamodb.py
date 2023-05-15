import boto3

from moto import mock_dynamodb


@mock_dynamodb
def create_mock_ddb_table():
    mock_ddb = boto3.resource('dynamodb')
    mock_ddb.create_table(
        TableName='PROFILE_TABLE',
        AttributeDefinitions=[
            {
                'AttributeName': 'pk',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'sk',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'pk',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'sk',
                'KeyType': 'RANGE'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    mock_ddb.Table('PROFILE_TABLE').put_item(
        Item={
            'pk': 'project',
            'sk': 'django-blog',
            'name': 'Django Blog'
        }
    )
