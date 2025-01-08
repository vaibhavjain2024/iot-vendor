import json
import os
from vendor.services.configuration_service import ConfigurationService
import aws_helper

# from logger_common import get_logger
# logger = get_logger()

def lambda_handler(event, context):
    """Lambda handler to update the vandor configuration."""   

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
        config_service.update_configuration(vendor_group, module, environment, secret_name, config_value)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Configuration updated successfully'})
        }
    except Exception as e:
        # logger.error("An exception occurred", exc_info=True)
        return aws_helper.lambda_response(status_code=400, data={}, msg=str(e))