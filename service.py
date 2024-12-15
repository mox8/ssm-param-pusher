import logging

import boto3

from settings import Settings
from utils import get_env_dict

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class AwsClientException(Exception):
    def __init__(self, message='Param push into the SSM Parameter Store failed'):
        self.message = message


class SsmParamPusherParamException(Exception):
    def __init__(
            self,
            message='Param push into the SSM Parameter Store failed\n'
                    'Check the following params in your settings:\n'
                    '\tACCESS_TOKEN\n'
                    '\tSECRET_ACCESS_KEY\n'
                    '\tREGION_NAME',
    ):
        self.message = message


class SsmParamPusher:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.session = self._get_session()
        self.ssm = self.session.client('ssm')

    def _get_session(self):
        try:
            return boto3.Session(
                aws_access_key_id=self.settings.ACCESS_TOKEN,
                aws_secret_access_key=self.settings.SECRET_ACCESS_KEY,
                region_name=self.settings.REGION_NAME,
            )
        except Exception as e:
            error_message = (
                'Unable to start AWS session.\nCheck the following params in your settings:\n'
                     '\tACCESS_TOKEN\n'
                     '\tSECRET_ACCESS_KEY\n'
                     '\tREGION_NAME'
            )
            logger.error(error_message)
            raise AwsClientException(error_message)

    def get_variable_name(self, variable_key):
        variable_name = str()
        if any([
            self.settings.NAMESPACE is not None,
            self.settings.STAGE is not None,
            self.settings.APP_NAME is not None,
        ]):
            if self.settings.NAMESPACE is not None:
                variable_name += f'/{self.settings.NAMESPACE}'
            if self.settings.STAGE is not None:
                variable_name += f'/{self.settings.STAGE}'
            if self.settings.APP_NAME is not None:
                variable_name += f'/{self.settings.APP_NAME}'
            variable_name += '/'
        variable_name += f'{variable_key}'
        return variable_name

    def set_variable(self, variable_key, variable_value):
        try:
            variable_name = self.get_variable_name(variable_key=variable_key)
            self.ssm.put_parameter(
                Name=variable_name,
                Value=variable_value,
                Type=self.settings.VARIABLES_TYPE,
                Overwrite=self.settings.OVERRIDE,
            )
            logger.info(f'Variable pushed: {variable_name}={variable_value}')

        except Exception as e:
            logger.info(f"Unexpected exceptions happened: {e}")
            raise SsmParamPusherParamException()

    def set_variables_from_file(self):
        for key, value in get_env_dict(env_filename=self.settings.ENV_FILE_NAME).items():
            self.set_variable(variable_key=key, variable_value=value)
