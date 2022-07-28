import boto3
from urllib import response
import requests
import yaml

def get_r53_client():
    """Gets you a r53 client
    """
    r53 = boto3.client('route53')

    return r53

def get_s3_client():
    """Gets you an s3 client
    """
    s3 = boto3.client('s3')

    return s3

def get_dynamic_ip():
    """Hits a stable (as of now at least) endpoint that returns your IP.
    """
    ip_url = "https://icanhazip.com"

    ip = requests.get(ip_url)
    return ip.text.rstrip()

# def get_hosted_zone(zone_list: list) -> list:
#     """Not actually sure why I wrote this. I think list_hosted_zones returns all I need."""
#     r53 = get_r53_client()

#     for zone in zone_list:
#         for domain in zone:
#             zone_details = r53.get_hosted_zone(
#                 Id=zone[domain]['id']
#             )
#             print(zone_details)

def get_self_hosted_domains(zone_list: list):
    """Pulls down a yaml file from s3 and returns the 'self_hosted' domains.
    """
    s3 = get_s3_client()
    static_file = s3.get_object(
        Bucket = "jh-lists",
        Key = "r53/r53_domains.yml"
    )
    #print(static_file)
    self_hosted = yaml.safe_load(static_file['Body'].read())
    for line in self_hosted['self_hosted']:
        get_records(line, zone_list)

def get_records(line: str, zone_list: list):
    """Accepts a domain from get_self_hosted_domains, looks up the A record from r53, then compares it
    to the current IP. If they are the same, stop here. If they are different, we'll update the A record
    to the current IP.
    """
    r53 = get_r53_client()
    current_ip = get_dynamic_ip()
    print(zone_list)
    print(line)
    #some code should go here to compare 'line' to 'zone_list' to pull out the 'line' hosted zone ID to
    # pass to list_resource_record_sets go get the A record
    
    a_record = r53.list_resource_record_sets(

    )

  



def list_hosted_zones():
    """Loops through the hosted zones in R53 and adds them to a dictionary.
    """
    r53 = get_r53_client()
    zone_list = []

    zones = r53.list_hosted_zones()

    for zone in zones['HostedZones']:
        zone_dict = { zone['Name']: { 'id':zone['Id'] }}
        zone_list.append(zone_dict)

    return zone_list


zone_list = list_hosted_zones()
get_self_hosted_domains(zone_list)
