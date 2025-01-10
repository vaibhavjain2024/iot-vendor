from repositories.configuration_repository import ConfigurationRepository

class ConfigurationService:
    def __init__(self, region_name):
        self.repo = ConfigurationRepository(region_name)

    def create_configuration(self, vendor_group, module, environment, secret_name, config_value):
        self.repo.create_configuration(vendor_group, module, environment, secret_name, config_value)

    def get_configuration(self, vendor_group, module, environment, secret_name):
        return self.repo.get_configuration(vendor_group, module, environment, secret_name)

    def update_configuration(self, vendor_group, module, environment, secret_name, config_value):
        self.repo.update_configuration(vendor_group, module, environment, secret_name, config_value)

    def delete_configuration(self, vendor_group, module, environment, secret_name):
        self.repo.delete_configuration(vendor_group, module, environment, secret_name)