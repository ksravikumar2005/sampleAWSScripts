#This script checks for ec2 instance or system status checks and sends a notification to SNS topic.
import json
import boto3
from pprint import pprint
client_ec2 = boto3.client('ec2', region_name='us-east-1')
client_sns = boto3.client('sns', region_name='us-east-1')

def lambda_handler(event, context):
    final_map = []
    status = client_ec2.describe_instance_status(IncludeAllInstances = True)
    pprint(status)
    for instance_status_entity in status['InstanceStatuses']:
        if('Details' in instance_status_entity['InstanceStatus']):
            instance_status_details = instance_status_entity['InstanceStatus']['Status']
            system_status_details = instance_status_entity['SystemStatus']['Details'][0]['Status']
            pprint(system_status_details)
            if instance_status_details != 'ok' or system_status_details != 'passed':
                final_map_entity = {}
                final_map_entity['instance_id'] = instance_status_entity['InstanceId']
                final_map_entity['instance_status'] = instance_status_details
                final_map_entity['system_status'] = system_status_details
                final_map.append(final_map_entity)
    response = client_sns.publish(TopicArn = 'arn:aws:region_name:xxxxxxx:sns_topic_name', Message=json.dumps(final_map))
    return final_map
