import abc


class PynjectorMain(abc.ABC):

    @abc.abstractmethod
    def main(self, args: list[str]):
        pass
