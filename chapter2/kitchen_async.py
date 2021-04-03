import asyncio

class CoroBot():
  def __init__(self):
    self.cutlery = Cutlery(knives=0, forks=0)
    self.tasks = asyncio.Queue()

  async def manage_table(self):
    while True:
#      This is the main point: the only places at which execution can switch between different CoroBot instances is where the await keyword appears. It is not possible to have a context switch during the rest of this function, and this is why there is no race condition during the modification of the kitchen cutlery inventory. The presence of await keywords makes context switches observable. This makes it significantly easier to reason about any potential race conditions in concurrent applications. This version of the code always passes the test, no matter how many tasks are assigned.
      task = await self.tasks.get()
      if task == 'prepare table':
        kitchen.give(to=self.cutlery, knives=4, forks=4)
      elif task == 'clear table':
        self.cutlery.give(to=kitchen, knives=4, forks=4)
      elif task == 'shutdown':
        return

from attr import attrs, attrib

@attrs
class Cutlery:
    knives = attrib(default=0)
    forks = attrib(default=0)

    def give(self, to: 'Cutlery', knives=0, forks=0):
        self.change(-knives, -forks)
        to.change(knives, forks)

    def change(self, knives, forks):
            self.knives += knives
            self.forks += forks

kitchen = Cutlery(knives=100, forks=100)
bots = [CoroBot() for i in range(10)]

import sys
for b in bots:
    for i in range(int(sys.argv[1])):
        b.tasks.put_nowait('prepare table')
        b.tasks.put_nowait('clear table')
    b.tasks.put_nowait('shutdown')

print('Kitchen inventory before service:', kitchen)

loop = asyncio.get_event_loop()
tasks = []
for b in bots:
    t = loop.create_task(b.manage_table())
    tasks.append(t)

task_group = asyncio.gather(*tasks)
loop.run_until_complete(task_group)
print('Kitchen inventory after service:', kitchen)