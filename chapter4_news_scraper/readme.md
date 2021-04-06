On your local machine, launch splash through docker

$ docker pull scrapinghub/splash
$ docker run --rm -p 8050:8050 scrapinghub/splash

On another terminal:
$ docker run -it python:3.8 bash

Now you will see the bash prompt of this new docker container running python3.8.
In this:
$  apt-get update
$  apt-get install vim
$  pip install aiohttp
$  pip install bs4
$  pip install lxml
$  python news.py &
Now you have a web server running inside this docker container on 8080.

$  wget http://localhost:8080/news
Inspect the output of the above wget. You will see the news items from cnn and aljazeera.