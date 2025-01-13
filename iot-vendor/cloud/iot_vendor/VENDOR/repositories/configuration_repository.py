import boto3
import json

class ConfigurationRepository:
    def __init__(self, region_name):
        self.ssm_client = boto3.client('ssm', region_name=region_name)

    def create_configuration(self, vendor_group, module, environment, secret_name, config_value, secure=True):
        parameter_name = f"/{vendor_group}/{module}/{environment}/{secret_name}"
        if isinstance(config_value, dict):
            # Store JSON data with a type indicator
            config_value_str = json.dumps(config_value)
            config_value_str = f"json:{config_value_str}"
        else:
            # Store plain string data with a type indicator
            config_value_str = f"str:{config_value}"

        param_type = 'SecureString' if secure else 'String'
        self.ssm_client.put_parameter(
            Name=parameter_name,
            Value=config_value_str,
            Type=param_type,
            Overwrite=True
        )

    def get_configuration(self, vendor_group, module, environment, secret_name):
        parameter_name = f"/{vendor_group}/{module}/{environment}/{secret_name}"
        response = self.ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        config_value_str = response['Parameter']['Value']
        
        # Check the type indicator and parse the data accordingly
        if config_value_str.startswith("json:"):
            return json.loads(config_value_str[5:])
        elif config_value_str.startswith("str:"):
            return config_value_str[4:]
        else:
            return config_value_str
    

    def update_configuration(self, vendor_group, module, environment, secret_name, config_value, secure=True):
        parameter_name = f"/{vendor_group}/{module}/{environment}/{secret_name}"
        if isinstance(config_value, dict):
            # Store JSON data with a type indicator
            config_value_str = json.dumps(config_value)
            config_value_str = f"json:{config_value_str}"
        else:
            # Store plain string data with a type indicator
            config_value_str = f"str:{config_value}"

        param_type = 'SecureString' if secure else 'String'
        self.ssm_client.put_parameter(
            Name=parameter_name,
            Value=config_value_str,
            Type=param_type,
            Overwrite=True
        )

    def delete_configuration(self, vendor_group, module, environment, secret_name):
        parameter_name = f"/{vendor_group}/{module}/{environment}/{secret_name}"
        self.ssm_client.delete_parameter(
            Name=parameter_name
        )