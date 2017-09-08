# Introduction
Web daemon for [ssmanager](https://github.com/sorz/ssmanager), which supports multi methods for different ports.
Be able to log traffic to influxdb, which can be nicely viewed by grafana.

# Install via pip3

    pip install git+https://github.com/shadowsocks/shadowsocks.git@master
    pip install git+https://github.com/sorz/ssmanager.git
    pip install git+https://github.com/fzinfz/ssmanager-nopanel.git

# Docker
Replace `fzinfz/ss:mgr-py` to `fzinfz/ss:mgr-pyForLibev` for libev version.

## Install docker
    curl -fsSL get.docker.com | bash

## Print Usage
    docker run --rm -it --net host fzinfz/ss:mgr-py ./main.py -h

## Demo - no traffic logging
### Start manager
    docker run --name ss-mgr -d --net host fzinfz/ss:mgr-py ./main.py

### check logs
    docker logs ss-mgr

### trigger config update
    curl http://localhost:8000/update

## Demo - log traffic to influxdb & display in grafana

    export IP_Private=127.0.0.1
    # Non-public IP suggested because no auth support for influxdb by default

    docker run --name influxdb \
        -p ${IP_Private}:8086:8086 \
        -v $PWD/influxdb:/var/lib/influxdb \
        -d --restart unless-stopped \
        influxdb   # Start influxdb

    curl -i -XPOST http://${IP_Private}:8086/query \
        --data-urlencode "q=CREATE DATABASE tsadmin"    # create db

    docker run --name ss-mgr -d --net host fzinfz/ss:mgr-py \
        ./main.py -d http://${IP_Private}:8086/write?db=tsadmin   # Start manager

    curl -G "http://${IP_Private}:8086/query?db=tsadmin&pretty=true" \
        --data-urlencode "q=SELECT * FROM ss GROUP BY * ORDER BY time DESC LIMIT 1"  # query latest traffic

    curl -G "http://${IP_Private}:8086/query?db=tsadmin&pretty=true" \
        --data-urlencode "q=SELECT count(\"value\") FROM ss GROUP BY *"  # count traffic items

    docker run -d --name grafana --net host grafana/grafana
    # Traffic dashboard: http://ip:3000, user/password:admin/admin

### Grafana query
    SELECT "value" FROM "ss" GROUP BY port

# Panel
This module works without a panel. It just read remote json file and write to influxdb.
But there is a panel exists for management: [https://github.com/fzinfz/tsadmin](https://github.com/fzinfz/tsadmin)

# Other notes
Only Python3.6 tested. Other 3.x versions may work. 2.x not supported.