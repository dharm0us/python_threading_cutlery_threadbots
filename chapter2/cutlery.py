from attr import attrs, attrib
import threading

@attrs
class Cutlery:
    knives = attrib(default=0)
    forks = attrib(default=0)
    lock = attrib(threading.Lock())

    def give(self, to: 'Cutlery', knives=0, forks=0):
        self.change(-knives, -forks)
        to.change(knives, forks)

    def change(self, knives, forks):
         with self.lock: #without this lock the count will be wrong
            self.knives += knives
            self.forks += forks

