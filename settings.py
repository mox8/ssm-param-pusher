import os
import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SettingsException(Exception):
    def __init__(self, message='Settings error'):
        self.message = message


class Settings:
    def __init__(self, settings_filename: str, required_fields: list[str]):
        full_settings_filename = os.path.join(os.getcwd(), settings_filename)
        with open(full_settings_filename, 'r') as f:
            data = json.load(f)
            for k, v in data.items():
                if v is not None:
                    setattr(self, k, v)
        self.validate_settings(required_fields=required_fields)
        logger.info('Settings Valid')

    def validate_settings(self, required_fields: list[str]):
        error_messages = list()
        for field in required_fields:
            if not hasattr(self, field):
                error_messages.append(f'{field} not set in settings file!')

        if error_messages:
            error_messages_string = '\n'.join(error_messages)
            logger.error(error_messages_string)
            raise SettingsException(error_messages_string)
