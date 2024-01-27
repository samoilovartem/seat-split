from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR: Path = Path(__file__).parents[1].resolve()


class Config(BaseSettings):
    skybox_endpoint: str = Field('https://skybox.vividseats.com/services/events', env='SKYBOX_ENDPOINT')
    sentinel_endpoint: str = Field('https://api.lewanddowski.com/scripts.php?token=', env='SENTINEL_ENDPOINT')
    sentinel_token: str = Field('', env='SENTINEL_TOKEN')
    stt_teams_endpoint: str = Field(
        'https://django-docker.herokuapp.com/api/v1/teams/', env='STT_TEAMS_ENDPOINT'
    )
    stt_auth_token: str = Field('', env='STT_AUTH_TOKEN')

    skybox_x_account: str = Field('', env='SKYBOX_X_ACCOUNT')
    skybox_x_application_token: str = Field('', env='SKYBOX_X_APPLICATION_TOKEN')
    skybox_x_api_token: str = Field('', env='SKYBOX_X_API_TOKEN')

    output_file: str = Field('events.csv', env='OUTPUT_FILE')

    sleep_time: int = Field(60, env='SLEEP_TIME')
    interval_time: int = Field(10, env='INTERVAL_TIME')

    team_venue_file: str = Field('team_and_home_venue.csv', env='TEAM_VENUE_FILE')

    @property
    def team_headers(self):
        return {
            'X-Account': self.skybox_x_account,
            'X-Application-Token': self.skybox_x_application_token,
            'X-Api-Token': self.skybox_x_api_token,
        }

    model_config = SettingsConfigDict(
        env_file=f'{str(ROOT_DIR)}/.env',
    )


config = Config()
