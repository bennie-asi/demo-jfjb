from threading import Timer
from threading import Thread

import pynput


class Monitor:
    def __init__(self, func):
        self.func = func
        # Thread(target=self.mouser).start()
        Thread(target=self.keyboarder).start()

    def hook(self, *typ_names):
        for name in typ_names:
            yield (lambda typ: (lambda *args: self.func(typ, *args)))(name)

    def mouser(self):
        with pynput.mouse.Listener(*self.hook('move', 'click', 'scroll')) as self.ml:
            self.ml.join()

    def keyboarder(self):
        with pynput.keyboard.Listener(*self.hook('press', 'release')) as self.kl:
            self.kl.join()

    def close(self):
        pynput.keyboard.Listener.stop(self.kl)
        pynput.mouse.Listener.stop(self.ml)


class MyTimer:
    def __init__(self, func):
        self.func = func
        self.th = Timer(0, int)

    def wait(self, seconds):  # only last timer work.
        self.th.cancel()
        self.th = Timer(seconds, self.timeout)
        self.th.start()

    def timeout(self):
        self.func()


if __name__ == '__main__':
    timer = MyTimer(lambda: print('No actions in 5 seconds!'))
    Monitor(lambda *_: timer.wait(5))
