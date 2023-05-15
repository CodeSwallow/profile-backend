import os
import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_projects_handler(event, context):
    """
    Gets projects from DynamoDB

    :param event: The event data passed to the Lambda function.
    :param context: The runtime information of the Lambda function.
    :return: A dictionary containing the response data.
    """

    try:
        logger.info("Event: {}".format(event))

        table_name = os.getenv('PROJECTS_TABLE')
        if not table_name:
            raise Exception('Table name missing')

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        items = table.scan()

        logger.info('DDB Response: {}'.format(items))

        return {
            'statusCode': 200,
            'body': json.dumps(items['Items'])
        }

    except Exception as error:
        logger.info('Error: {}'.format(error))

        return {
            "statusCode": 500,
            'body': json.dumps({'message': 'Internal Server Error'})
        }
