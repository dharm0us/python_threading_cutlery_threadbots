from threadbot import ThreadBot
import sys
from cutlery import Cutlery

kitchen = Cutlery(knives=100, forks=100)
bots = [ThreadBot(kitchen) for i in range(10)]

for bot in bots:
    for i in range(int(sys.argv[1])):
        bot.tasks.put('prepare table')
        bot.tasks.put('clear table')
    bot.tasks.put('shutdown')

print('Kitchen inventory before service:', kitchen)
for bot in bots:
    bot.start()

for bot in bots:
    bot.join()
print('Kitchen inventory after service:', kitchen)