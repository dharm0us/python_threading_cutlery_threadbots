'''
Our toy message broker works. The code is also pretty easy to understand, given such a complex problem domain, but unfortunately, the design of the broker code itself is problematic.

The problem is that, for a particular client, we send messages to subscribers in the same coroutine as where new messages are received. This means that if any subscriber is slow to consume what we’re sending, it might take a long time for that await gather(...) line in Example 4-2 to complete, and we cannot receive and process more messages while we wait.

Instead, we need to decouple the receiving of messages from the sending of messages. In the next case study, we refactor our code to do exactly that.
'''
import asyncio
from asyncio import StreamReader, StreamWriter, gather
from collections import deque, defaultdict
from typing import Deque, DefaultDict
from msgproto import read_msg, send_msg

SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)
'''Each client establishes a connection by sending a channel name to subscribe to. Then sends messages with channel_name and data.'''
async def client(reader: StreamReader, writer: StreamWriter):
  peername = writer.get_extra_info('peername')
  subscribe_chan = await read_msg(reader)
  SUBSCRIBERS[subscribe_chan].append(writer)
  print(f'Remote {peername} subscribed to {subscribe_chan}')
  try:
    while channel_name := await read_msg(reader):
      data = await read_msg(reader)
      print(f'Sending to {channel_name}: {data[:19]}...')
      conns = SUBSCRIBERS[channel_name]
      if conns and channel_name.startswith(b'/queue'):
          conns.rotate() #using deque comes in handy as rotate is O(1)
          conns = [conns[0]]
      await gather(*[send_msg(c, data) for c in conns])
      '''This line is a bad flaw in our program, but it may not be obvious why: though it may be true that all of the sending to each subscriber will happen concurrently, what happens if we have one very slow client? In this case, the gather() will finish only when the slowest subscriber has received its data. We can’t receive any more data from the sending client until all these send_msg() coroutines finish. This slows all message distribution to the speed of the slowest subscriber.
      '''
  except asyncio.CancelledError:
    print(f'Remote {peername} closing connection.')
    writer.close()
    await writer.wait_closed()
  except asyncio.IncompleteReadError:
    print(f'Remote {peername} disconnected')
  finally:
    print(f'Remote {peername} closed')
    SUBSCRIBERS[subscribe_chan].remove(writer)
    '''When leaving the client() coroutine, we make sure to remove ourselves from the global SUBSCRIBERS collection. Unfortunately, this is an O(n) operation, which can be a little expensive for very large n. A different data structure would fix this, but for now we console ourselves with the knowledge that connections are intended to be long-lived—thus, there should be few disconnection events—and n is unlikely to be very large (say ~10,000 as a rough order-of-magnitude estimate), and this code is at least easy to understand.'''

async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()

try:
    asyncio.run(main(client, host='127.0.0.1', port=25000))
except KeyboardInterrupt:
    print('Bye!')