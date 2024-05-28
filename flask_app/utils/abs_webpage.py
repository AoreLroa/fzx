from abc import ABC, abstractmethod


class BaseWebPage(ABC):

    @abstractmethod
    def method(self):
        pass

    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def headers(self):
        pass

    @abstractmethod
    def data(self):
        pass

    @abstractmethod
    def params(self):
        pass

    @abstractmethod
    def parse_response(self, data):
        pass
