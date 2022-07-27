from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

import requests


@dataclass
class Property(ABC):
    property: str
    dtype: str

    def __post_init__(self) -> None:
        # changing parent class after dataclass init
        self.__class__ = eval(self.dtype.capitalize())

    @property
    def name(self):
        return self.__class__.__name__.lower()

    def __call__(self, condition_obj):
        return {'property': self.property, self.name: condition_obj}


class Number(Property):
    # Number filter methods
    # See: https://developers.notion.com/reference/post-database-query-filter#number-filter-condition
    def __init__(self, *args):
        super().__init__(*args, self.__class__)

    def __eq__(self, number):
        return self({'equals': number})

    def __ne__(self, number):
        return self({'does_not_equal': number})

    def __gt__(self, number):
        return self({'greater_than': number})

    def __lt__(self, number):
        return self({'less_than': number})

    def __ge__(self, number):
        return self({'greater_than_or_equal_to': number})

    def __le__(self, number):
        return self({'less_than_or_equal_to': number})

    def is_empty(self):
        return self({'is_empty': True})

    def is_not_empty(self):
        return self({'is_not_empty': True})


def query_database(id, token, filter_payload):
    endpoint = f"https://api.notion.com/v1/databases/{id}/query"

    payload = {'filter': filter_payload}
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(endpoint, json=payload, headers=headers)
    return response.json().get('results')
