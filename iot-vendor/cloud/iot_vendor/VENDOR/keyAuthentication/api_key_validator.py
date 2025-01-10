import boto3
from botocore.exceptions import ClientError
from .base_validator import BaseValidator

class APIKeyValidator(BaseValidator):
    def __init__(self, region_name=None):
        self.region_name = region_name or 'ap-south-1'
        self.api_keys = self._get_all_api_keys()

    def _get_all_api_keys(self):
        client = boto3.client('apigateway', region_name=self.region_name)
        api_keys = {}
        try:
            paginator = client.get_paginator('get_api_keys')
            for page in paginator.paginate(includeValues=True):
                for key in page.get('items', []):
                    api_keys[key['id']] = key['value']
            return api_keys
        except ClientError as e:
            raise Exception("Error retrieving API keys: " + str(e))

    def validate(self, api_key):
        if api_key not in self.api_keys.values():
            raise Exception("Unauthorized")