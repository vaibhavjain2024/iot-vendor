import json
import os
from VENDOR.services.configuration_service import ConfigurationService
from VENDOR.keyAuthentication.common.decorators import api_key_auth
from VENDOR.keyAuthentication.api_key_validator import APIKeyValidator
import aws_helper

# from logger_common import get_logger
# logger = get_logger()

@api_key_auth(APIKeyValidator)
def create_configuration(event, service, vendor_group, module, environment, secret_name, config_value):
    service.create_configuration(vendor_group, module, environment, secret_name, config_value)

def lambda_handler(event, context):
    """Lambda handler to create the vandor configuration."""    
    
    query_params = event.get("queryStringParameters", {})

    # logger.info(f"Query Params :: {query_params}")

    vendor_group = query_params.get("vendor_group")
    module = query_params.get("module")
    environment = query_params.get("environment", "dev")
    secret_name = query_params.get("secret_name")
    config_value = query_params.get("config_value")

    region_name = query_params.get('region_name', os.environ.get("REGION", "ap-south-1"))

    if not all([vendor_group, module, environment, secret_name, config_value]):
        return aws_helper.lambda_response(status_code=400, data={}, msg="All parameters are mandatory: vendor_group, module, environment, secret_name, config_value")

    config_service = ConfigurationService(region_name)
    
    try:
        create_configuration(event, service=config_service, vendor_group=vendor_group, module=module, environment=environment, secret_name=secret_name, config_value=config_value)
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Configuration created successfully'})
        }
    except Exception as e:
        # logger.error("An exception occurred", exc_info=True)
        return aws_helper.lambda_response(status_code=400, data={}, msg=str(e))