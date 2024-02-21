from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    skybox_endpoint: str = 'https://skybox.vividseats.com/services'
    skybox_events_prefix: str = '/events/'
    skybox_purchases_prefix: str = '/purchases/'

    skybox_x_account: str = Field('', env='SKYBOX_X_ACCOUNT')
    skybox_x_application_token: str = Field('', env='SKYBOX_X_APPLICATION_TOKEN')
    skybox_x_api_token: str = Field('', env='SKYBOX_X_API_TOKEN')

    stt_endpoint: str = 'https://sttdjangobackend-production.up.railway.app/api/v1'
    stt_teams_prefix: str = '/teams/'
    stt_seasons_prefix: str = '/seasons/'
    stt_auth_token: str = Field('', env='STT_AUTH_TOKEN')

    tiqassist_endpoint: str = 'https://app.tiqassist.com/api/registration/options'

    @property
    def get_skybox_api_headers(self):
        return {
            'X-Account': self.skybox_x_account,
            'X-Application-Token': self.skybox_x_application_token,
            'X-Api-Token': self.skybox_x_api_token,
        }

    @property
    def get_skybox_events_endpoint(self):
        return f'{self.skybox_endpoint}{self.skybox_events_prefix}'

    @property
    def get_skybox_purchases_endpoint(self):
        return f'{self.skybox_endpoint}{self.skybox_purchases_prefix}'

    @property
    def get_stt_teams_endpoint(self):
        return f'{self.stt_endpoint}{self.stt_teams_prefix}'

    @property
    def get_stt_authorization_header(self):
        return {'Authorization': f'Token {self.stt_auth_token}'}

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
