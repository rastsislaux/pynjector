from pynjector import defaultctx


@defaultctx.singleton()
class Bean2:

    def __repr__(self):
        return "Bean2()"
