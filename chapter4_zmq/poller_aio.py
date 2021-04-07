# poller_aio.py
import asyncio
import zmq
from zmq.asyncio import Context

context = Context()

async def do_receiver_works_only_when_client_starts_after_server():
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5557")
    while message := await receiver.recv_json():
        print(f'Via PULL: {message}')

async def do_receiver_works_whether_client_or_server_starts_first():
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5557")
    while True:
        message = await receiver.recv_json()
        if message:
            print(f'Via PULL: {message}')
        else:
            continue


async def do_subscriber_works_only_when_client_starts_after_server():
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5556")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
    while message := await subscriber.recv_json():
        print(f'Via SUB: {message}')

async def do_subscriber_works_whether_client_or_server_starts_first():
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5556")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
    while True:
        message = await subscriber.recv_json()
        if message:
            print(f'Via SUB: {message}')
        else:
            continue

async def main():
    await asyncio.gather(
        #do_receiver_works_whether_client_or_server_starts_first(),
        #do_subscriber_works_whether_client_or_server_starts_first(),
        do_receiver_works_only_when_client_starts_after_server(),
        do_subscriber_works_only_when_client_starts_after_server(),
    )

asyncio.run(main())