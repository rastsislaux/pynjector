from Bean2 import Bean2
from pynjector import defaultctx


@defaultctx.singleton()
class Bean1:

    def __init__(self, bean2: Bean2):
        self.bean2 = bean2

    def __repr__(self):
        return f"Bean1(bean2={self.bean2})"
