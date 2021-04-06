$ docker run -it python:3.8 bash

Now you will see the bash prompt of this new docker container running python3.8.
In this:
$ pip install zmq
$ python poller.py &
$ python poller_srv.py
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
Ideally poller_aio.py should work the same way but I couldn't make it work.