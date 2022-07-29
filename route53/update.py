# import boto3
# from urllib import response
# import requests
import yaml
import main

def get_self_hosted_domains(zone_list: list):
    """Pulls down a yaml file from s3 and returns the 'self_hosted' domains.
    """

    static_file = main.get_s3_client().get_object(
        Bucket = "jh-lists",
        Key = "r53/r53_domains.yml"
    )
    self_hosted = yaml.safe_load(static_file['Body'].read())
    for line in self_hosted['self_hosted']:
        get_records(line, zone_list)

def update_record(zone_id: str, my_domain: str):
    change_status = main.get_r53_client().change_resource_record_sets(
        HostedZoneId = zone_id,
        ChangeBatch = {
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': my_domain,
                        'Type': 'A',
                        'TTL': 60,
                        'ResourceRecords': [
                            {
                                'Value': main.get_dynamic_ip()
                            }
                        ]
                    }
                }
            ]
        }
    )
    print(change_status)

def get_records(line: str, zone_list: list):
    """Accepts a domain from get_self_hosted_domains, looks up the A record from r53, then compares it
    to the current IP. If they are the same, stop here. If they are different, we'll update the A record
    to the current IP.
    """

    for domain in zone_list:
        for my_domain in domain.keys():
            if my_domain == line + '.':
                zone_id = zone_list[0][my_domain]["id"].split('/')[2]
   
                a_record = main.get_r53_client().list_resource_record_sets(
                    HostedZoneId = zone_id,
                )
                r53_ip = a_record['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']
                if r53_ip == main.get_dynamic_ip():
                    print('IP matches. No updates required')
                    update_record(zone_id, my_domain) #for testing
                else:
                    print('No match. This needs updated.')
                    update_record(zone_id, my_domain)

def list_hosted_zones():
    """Loops through the hosted zones in R53 and adds them to a dictionary.
    """

    zone_list = []

    zones = main.get_r53_client().list_hosted_zones()

    for zone in zones['HostedZones']:
        zone_dict = { zone['Name']: { 'id':zone['Id'] }}
        zone_list.append(zone_dict)

    return zone_list


# zone_list = list_hosted_zones()
get_self_hosted_domains(list_hosted_zones())
