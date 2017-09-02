# Introduction
Web hook for [ssmanager](https://github.com/sorz/ssmanager)

# Requirement
```
pip install git+https://github.com/shadowsocks/shadowsocks.git@master
pip install git+https://github.com/sorz/ssmanager.git
```

# Docker
```
docker run --rm -it --net host fzinfz/ss:mgr-py ./main.py -h  # Print Usage

# Demo
docker run --name ss-mgr -d --net host fzinfz/ss:mgr-py ./main.py   # Start manager 
docker logs ss-mgr                      # check logs
curl http://localhost:8000/update       # update ss servers
```
