# Introduction
Web daemon for [ssmanager](https://github.com/sorz/ssmanager), which supports multi methods for different ports.
Use influxdb for traffic logging.

# Requirement
Python3.6+

    pip install git+https://github.com/shadowsocks/shadowsocks.git@master
    pip install git+https://github.com/sorz/ssmanager.git


# Demo
## Install docker
    curl -fsSL get.docker.com | bash

## Print Usage
    docker run --rm -it --net host fzinfz/ss:mgr-py ./main.py -h

## Demo - no traffic logging
    docker run --name ss-mgr -d --net host fzinfz/ss:mgr-py ./main.py   # Start manager
    docker logs ss-mgr                      # check logs
    curl http://localhost:8000/update       # trigger config update

## Demo - traffic logging to influxdb
    export IP_Private=127.0.0.1   # Non-public IP
    docker run --name influxdb -p ${IP_Private}:8086:8086 -d influxdb   # Start influxdb
    curl -i -XPOST http://${IP_Private}:8086/query --data-urlencode "q=CREATE DATABASE tsadmin"    # create db
    docker run --name ss-mgr -d --net host fzinfz/ss:mgr-py ./main.py -d http://${IP_Private}:8086/write?db=tsadmin   # Start manager
    curl -G "http://${IP_Private}:8086/query?db=tsadmin&pretty=true" --data-urlencode "q=SELECT * FROM ss GROUP BY * ORDER BY time DESC LIMIT 1"  # query latest traffic
    curl -G "http://${IP_Private}:8086/query?db=tsadmin&pretty=true" --data-urlencode "q=SELECT count(\"value\") FROM ss GROUP BY *"  # count traffic items
    docker run -d --name=grafana --net host grafana/grafana # traffic dashboard http://ip:3000, user/password:admin/admin