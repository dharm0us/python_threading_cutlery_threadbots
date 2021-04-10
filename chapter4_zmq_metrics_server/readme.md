docker run -it -p8088:8088 python:3.8 bash
apt-get update
pip install zmq
apt-get install vim
pip install zmq.asyncio
pip install aiohttp
pip install aiohttp_sse
pip install psutil

python metrics_server.py &
python metrics_producer_app.py --color red & 
python metrics_producer_app.py --color blue --leak 10000 &
python metrics_producer_app.py --color green --leak 1000000 &

Then on the browser http://127.0.0.1:8088 will show you the metrics.