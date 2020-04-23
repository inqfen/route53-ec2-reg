import boto3
from ec2_metadata import ec2_metadata
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--instance_name', action='store', type=str)
parser.add_argument('--zone_id', action='store', type=str)

args = parser.parse_args()

INSTANCE_NAME = args.instance_name
ZONE_ID = args.zone_id

instance_ip = ec2_metadata.public_ipv4()
if not len(instance_ip):
    print('Instance have not public ip')

boto_client = boto3.client('route53')

change_record = boto_client.change_resource_record_sets(
    HostedZoneId=ZONE_ID,
    ChangeBatch = {
        'Comment': 'Autocreated record',
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': INSTANCE_NAME,
                    'Type': 'A',
                    'TTL': 600,
                    'ResourceRecords': [
                    {
                        'Value': instance_ip
                    }
                    ]
                }
            }
        ]
    }
)
