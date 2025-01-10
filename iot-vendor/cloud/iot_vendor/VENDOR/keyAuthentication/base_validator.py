
class BaseValidator:
    def validate(self, api_key):
        raise NotImplementedError("Subclasses should implement this method")