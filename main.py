from Bean1 import Bean1
from pynjector import PynjectorMain, defaultctx


@defaultctx.singleton()
class Main(PynjectorMain):

    def __init__(self, bean1: Bean1, bean2):
        self.bean1 = bean1
        self.bean2 = bean2

    def main(self, args: list[str]):
        print(self.bean1)
        print(self.bean2)


if __name__ == '__main__':
    defaultctx.init()
