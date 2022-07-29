import boto3
import requests

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