# Introduction
Web hook for [ssmanager](https://github.com/sorz/ssmanager)
# Requirement
```
pip install git+https://github.com/shadowsocks/shadowsocks.git@master
pip install git+https://github.com/sorz/ssmanager.git
```

# Docker
```
docker run --rm -it --net host fzinfz/ss:mgr-py ./main.py -h
docker run --rm -it --net host fzinfz/ss:mgr-py ./main.py
```

# Sample json file
```
[{"port": 8001, "password": "test123", "method": "chacha20"},
 {"port": 8002, "password": "123test", "method": "aes-256-cfb"}]
```
