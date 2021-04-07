$ docker run -it python:3.8 bash

Now you will see the bash prompt of this new docker container running python3.8.
In this:

$ pip install zmq

With normal Zmq(i.e. without asyncio), you can start the client before the server or vice versa. Since the polling goes on in the infinite loop.
So
Either
$ python poller.py &
$ python poller_srv.py &

OR
$ python poller_srv.py &
$ python poller.py &

will work.

But with async implementation, in the original code you have to start the server before the client else the client would get stuck and won't be able to come out of the loop.

So only
$ python poller_srv.py &
$ python poller_aio.py &

would work.

But I have made some changes in poller_aio.py and you can see both the code versions - one of them will work irrespective of the starting order of client/server. The other is still dependent.

Via PULL: 0
Via SUB: 0
Via PULL: 1
Via SUB: 1
Via PULL: 2
Via SUB: 2
Via PULL: 3
Via SUB: 3
Via PULL: 4
Via SUB: 4

-----------------
