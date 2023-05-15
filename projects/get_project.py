import os
import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_project_handler(event, context):
    """
    Gets project from DynamoDB by project_id

    :param event: The event data passed to the Lambda function.
    :param context: The runtime information of the Lambda function.
    :return: A dictionary containing the response data.
    """
    partition_key = 'project'

    try:
        logger.info("Event: {}".format(event))

        table_name = os.getenv('PROFILE_TABLE')
        if not table_name:
            raise Exception('Table name missing')

        try:
            project_id = event['pathParameters']['project_id']
        except KeyError as error:
            logger.info('Error: {}'.format(error))

            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Bad Request'})
            }

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        item = table.get_item(
            Key={
                'pk': partition_key,
                'sk': project_id
            }
        )

        logger.info('DDB Response: {}'.format(item))

        return {
            'statusCode': 200,
            'body': json.dumps(item['Item'])
        }

    except Exception as error:
        logger.info('Error: {}'.format(error))

        return {
            "statusCode": 500,
            'body': json.dumps({'message': 'Internal Server Error'})
        }
