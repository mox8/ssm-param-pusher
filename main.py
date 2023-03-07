import logging

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
    CONFIG_FILENAME = 'config.json'
    REQUIRED_CONFIG_PARAMS = [
        'ENV_FILE_NAME',
        'REGION_NAME',
        'ACCESS_TOKEN',
        'SECRET_ACCESS_KEY',
        'VARIABLES_TYPE',
        'OVERRIDE',
    ]

    app_settings = Settings(
        settings_filename=CONFIG_FILENAME,
        required_fields=REQUIRED_CONFIG_PARAMS,
    )

    runner = Runner(settings=app_settings)
    runner.run()
