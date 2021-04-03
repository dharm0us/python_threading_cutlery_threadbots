# python_threading_cutlery_threadbots
code for the book: https://learning.oreilly.com/library/view/using-asyncio-in/9781492075325/ch02.html
chapter 2.

$ python main.py 100
Kitchen inventory before service: Cutlery(knives=100, forks=100)
Kitchen inventory after service: Cutlery(knives=100, forks=100)

$ python main.py 1000
Kitchen inventory before service: Cutlery(knives=100, forks=100)
Kitchen inventory after service: Cutlery(knives=100, forks=100)

$ python main.py 10000 - problem!! - inventory doesn't match
Kitchen inventory before service: Cutlery(knives=100, forks=100)
Kitchen inventory after service: Cutlery(knives=88, forks=100)

It will be resolved if you add lock in cutlery class.
Or you could use async version:

$ python kitchen_async.py 10000
Kitchen inventory before service: Cutlery(knives=100, forks=100)
Kitchen inventory after service: Cutlery(knives=100, forks=100)