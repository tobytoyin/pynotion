import requests
import os
from dataclasses import dataclass
from .dataclasses import Page


class App:
    # App starting class
    token: str

    @property
    def end_point(self):
        return 'https://api.notion.com/v1/'

    @property
    def headers(cls):
        return {
            'accept': 'application/json',
            'Notion-Version': "2022-06-28",
            'Authorization': f'Bearer {cls.token}',
        }


@dataclass
class DatabaseConnector:
    api_route = 'databases'
    uid: str

    @property
    def connection_url(self):
        return os.path.join(App().end_point, self.api_route, self.uid)

    @property
    def query_url(self):
        return os.path.join(App().end_point, self.api_route, self.uid, 'query')

    def get(self) -> requests.Response:
        return requests.get(self.connection_url, headers=App.headers)

    def get_pages(self):
        payload = {"page_size": 1000}
        headers = {**App().headers, "content-type": "application/json"}

        try:
            responses = requests.post(self.query_url, json=payload, headers=headers)
            pages = responses.json().get('results')

        except Exception as e:
            raise e

        return [PageConnector(url=page.get('url'), id=page.get('id')) for page in pages]


class PageConnector(Page):
    api_route = 'pages'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cached_contents = None

    @property
    def connection_url(self):
        return os.path.join(App().end_point, self.api_route, self.id)

    @property
    def contents(self):
        """Contents of a Notion Page object

        Returns:
            _type_: _description_
        """
        if not self.cached_contents:
            resposne = requests.get(self.connection_url, headers=App().headers)
            self.cached_contents = resposne

        return self.cached_contents
