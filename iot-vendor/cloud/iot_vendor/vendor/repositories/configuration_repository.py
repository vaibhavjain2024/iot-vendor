import boto3

class ConfigurationRepository:
    def __init__(self, region_name):
        self.ssm_client = boto3.client('ssm', region_name=region_name)

    def create_configuration(self, vendor_group, module, environment, secret_name, config_value):
        parameter_name = f"/{vendor_group}/{module}/{environment}/{secret_name}"
        self.ssm_client.put_parameter(
            Name=parameter_name,
            Value=config_value,
            Type='String',
            Overwrite=True
        )

    def get_configuration(self, vendor_group, module, environment, secret_name):
        parameter_name = f"/{vendor_group}/{module}/{environment}/{secret_name}"
        response = self.ssm_client.get_parameter(
            Name=parameter_name
        )
        return response['Parameter']['Value']

    def update_configuration(self, vendor_group, module, environment, secret_name, config_value):
        parameter_name = f"/{vendor_group}/{module}/{environment}/{secret_name}"
        self.ssm_client.put_parameter(
            Name=parameter_name,
            Value=config_value,
            Type='String',
            Overwrite=True
        )

    def delete_configuration(self, vendor_group, module, environment, secret_name):
        parameter_name = f"/{vendor_group}/{module}/{environment}/{secret_name}"
        self.ssm_client.delete_parameter(
            Name=parameter_name
        )