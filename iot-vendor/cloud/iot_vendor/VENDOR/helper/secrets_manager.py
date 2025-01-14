import boto3
import json
class SecretManager:
    def __init__(self, secret_manager_key, region):
        self.region = region
        self.secret_arn = secret_manager_key
        self.secret_client = boto3.client('secretsmanager', self.region)

    def get_db_string(self, vendor_name):
        get_secret_value_response = self.secret_client.get_secret_value(SecretId=self.secret_arn)
        secret_value = json.loads(get_secret_value_response['SecretString']).get(vendor_name)
        return secret_value