from dataclasses import dataclass
from abc import ABC


class Block(ABC):
    @property
    def name(self):
        return self.__class__.__name__.lower()

    @property
    def type_object(self) -> dict:
        ...

    def __call__(self):
        return {'type': self.name, self.name: self.type_object}


@dataclass
class Text(Block):
    content: str
    link: str = None

    @property
    def type_object(self) -> dict:
        return {
            'content': self.content,
            'link': self.link,
        }


@dataclass
class Heading(Text):
    level: int = 1

    @property
    def name(self):
        return f'{super().name}_{self.level}'

    @property
    def type_object(self):
        text_obj = super().type_object  # init Text(...)
        return {'rich_text': [text_obj]}


@dataclass
class Toggle(Text):
    @property
    def type_object(self):
        text_obj = super().type_object  # init Text(...)
        return {'rich_text': [text_obj]}
