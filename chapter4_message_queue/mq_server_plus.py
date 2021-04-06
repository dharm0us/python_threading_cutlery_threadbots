# mq_server_plus.py
import asyncio
from asyncio import StreamReader, StreamWriter, Queue
from collections import deque, defaultdict
from contextlib import suppress
from typing import Deque, DefaultDict, Dict
from msgproto import read_msg, send_msg

CHANNEL_TO_SUBSCRIBERS_MAP: DefaultDict[bytes, Deque] = defaultdict(deque)
CLIENT_TO_MSGS_MAP: DefaultDict[StreamWriter, Queue] = defaultdict(Queue)
CHANNEL_TO_MSGS_MAP: Dict[bytes, Queue] = {}

async def client(reader: StreamReader, writer: StreamWriter):
  peername = writer.get_extra_info('peername')
  subscribe_chan = await read_msg(reader)
  CHANNEL_TO_SUBSCRIBERS_MAP[subscribe_chan].append(writer)
  # remember that create_task submits the task to the event loop.
  # In that sense, create_task is a misnomer. It creates AND starts the task.
  send_task = asyncio.create_task(
      send_client(writer, CLIENT_TO_MSGS_MAP[writer]))
  print(f'Remote {peername} subscribed to {subscribe_chan}')
  try:
    # note the use of walrus operator(:=) here, introduced in py3.8
    # a = b is a statement whereas a := b is an expression which evaluates to b
    # and hence can be used by while to test its value.
    while channel_name := await read_msg(reader):
      data = await read_msg(reader)
      if channel_name not in CHANNEL_TO_MSGS_MAP:
        CHANNEL_TO_MSGS_MAP[channel_name] = Queue(maxsize=10)
        asyncio.create_task(chan_sender(channel_name))
      # in the line below we use asyncio Queue with size 10. It won't return
      # until we have been able to put this latest msg(i.e. data) onto it.
      # If there is no space in it, it will wait for the space to free up.
      # It also means that until this returns, more data won't be read.
      await CHANNEL_TO_MSGS_MAP[channel_name].put(data)
  except asyncio.CancelledError:
    print(f'Remote {peername} connection cancelled.')
  except asyncio.IncompleteReadError:
    print(f'Remote {peername} disconnected')
  finally:
    print(f'Remote {peername} closed')
    # putting None here so that in send_client, break is triggered
    await CLIENT_TO_MSGS_MAP[writer].put(None)
    await send_task
    del CLIENT_TO_MSGS_MAP[writer]
    CHANNEL_TO_SUBSCRIBERS_MAP[subscribe_chan].remove(writer)

async def send_client(writer: StreamWriter, client_msgs: Queue):
    while True:
        try:
            msg = await client_msgs.get()
        except asyncio.CancelledError:
            # we are ignoring this as we want to end it only by None in the queue
            continue
        # in the finally block above, None has been put into this Queue  
        if not msg:
            break

        try:
            await send_msg(writer, msg)
        except asyncio.CancelledError:
            await send_msg(writer, msg)

    writer.close()
    await writer.wait_closed()

async def chan_sender(channel_name: bytes):
    with suppress(asyncio.CancelledError):
        while True:
            writers = CHANNEL_TO_SUBSCRIBERS_MAP[channel_name]
            if not writers:
                # if there are no subscribers yet, wait and repeat in time.
                await asyncio.sleep(1)
                continue
            if channel_name.startswith(b'/queue'):
                writers.rotate()
                writers = [writers[0]]
            # we aren't putting None in this queue yet
            # so this path won't be triggered
            if not (msg := await CHANNEL_TO_MSGS_MAP[channel_name].get()):
                break
            for writer in writers:
                # the msg to these client is lost if the queue is full
                # penalty for being slow
                if not CLIENT_TO_MSGS_MAP[writer].full():
                    print(f'Sending to {channel_name}: {msg[:19]}...')
                    await CLIENT_TO_MSGS_MAP[writer].put(msg)

async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()
try:
    asyncio.run(main(client, host='127.0.0.1', port=25000))
except KeyboardInterrupt:
    print('Bye!')