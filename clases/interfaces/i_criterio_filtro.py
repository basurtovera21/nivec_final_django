from abc import ABCMeta 
from abc import abstractmethod


class ICriterioFiltro(metaclass = ABCMeta):
    @abstractmethod
    def es_valido(self, registro: dict):
        pass