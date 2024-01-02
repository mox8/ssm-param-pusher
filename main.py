import logging
import os
import argparse

from settings import (
    SettingsException,
    Settings,
)
from service import (
    SsmParamPusher,
    SsmParamPusherParamException,
)


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)
ENVIRONMENTS_DIR_NAME = 'environments'
DEFAULT_CONFIG_FILENAME = 'config.json'
DEFAULT_VARIABLES_FILENAME = 'vars.env'


def get_environment_file(environment_name: str, filename: str = None) -> str:
    return os.path.join(os.getcwd(), ENVIRONMENTS_DIR_NAME, environment_name, filename)


class Runner:
    ssm_param_pusher: SsmParamPusher.__class__ = SsmParamPusher
    exceptions = (
        SettingsException,
        SsmParamPusherParamException
    )

    def __init__(self, settings: Settings):
        self.ssm = self.ssm_param_pusher(settings=settings)

    def run(self):
        try:
            self.ssm.set_variables_from_file()
            logger.info('Finished successfully')

        except self.exceptions as e:
            logger.error(getattr(e, 'message', f'{e.__class__.__name__}: {e}'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--environment', type=str, required=True)

    args = parser.parse_args()
    environment = args.environment

    settings_file = get_environment_file(environment, DEFAULT_CONFIG_FILENAME)
    variables_file = get_environment_file(environment, DEFAULT_VARIABLES_FILENAME)

    if not os.path.exists(settings_file):
        raise FileNotFoundError(f'File {settings_file} not found')

    if not os.path.exists(variables_file):
        raise FileNotFoundError(f'File {variables_file} not found')

    REQUIRED_CONFIG_PARAMS = [
        'ENV_FILE_NAME',
        'REGION_NAME',
        'ACCESS_TOKEN',
        'SECRET_ACCESS_KEY',
        'VARIABLES_TYPE',
        'OVERRIDE',
    ]

    app_settings = Settings(
        full_settings_filename=settings_file,
        full_variables_filename=variables_file,
        required_fields=REQUIRED_CONFIG_PARAMS,
    )

    runner = Runner(settings=app_settings)
    runner.run()
