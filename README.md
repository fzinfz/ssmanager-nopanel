# Introduction
Web daemon for [ssmanager](https://github.com/sorz/ssmanager), which supports multi methods for different ports.  
Instead of checking port lists periodically, you need to trigger web hook manually for port info updating.  
You can enable logging traffic to InfluxDB, which can be nicely viewed in Grafana.

# Install via pip3

    pip3 install git+https://github.com/shadowsocks/shadowsocks.git@master
    pip3 install git+https://github.com/sorz/ssmanager.git
    pip3 install git+https://github.com/fzinfz/ssmanager-nopanel.git
    ssmanager-nopanel -h # print usage
    ssmanager-nopanel # run demo without traffic logging

Note: Only Python 3.6 tested. Other 3.x versions may work. 2.x not supported.

# Docker Demo
Log traffic to influxdb & display in grafana

## Install docker
    curl -fsSL get.docker.com | bash

## InfluxDB

    export IP_Private=127.0.0.1
    # Non-public IP suggested because influxdb auth not enabled by default

    docker run --name influxdb \
        -p ${IP_Private}:8086:8086 \
        -v $PWD/influxdb:/var/lib/influxdb \
        -d --restart unless-stopped \
        influxdb   # Start influxdb

    curl -i -XPOST http://${IP_Private}:8086/query \
        --data-urlencode "q=CREATE DATABASE tsadmin"    # create db

## ssmanager

    export URL_influxdb=http://${IP_Private}:8086/write?db=tsadmin

    docker run --name ss-mgr-py    -d --net host fzinfz/ss:mgr-py    -d $URL_influxdb  # ss Python version
    docker run --name ss-mgr-libev -d --net host fzinfz/ss:mgr-libev -d $URL_influxdb  # ss Libev version

    docker logs ss-mgr # check logs

## Check InfluxDB

    curl -G "http://${IP_Private}:8086/query?db=tsadmin&pretty=true" \
        --data-urlencode "q=SELECT * FROM ss GROUP BY * ORDER BY time DESC LIMIT 1"  # query latest traffic

    curl -G "http://${IP_Private}:8086/query?db=tsadmin&pretty=true" \
        --data-urlencode "q=SELECT count(\"value\") FROM ss GROUP BY *"  # count traffic items

## Grafana

    docker run -d --name grafana --net host grafana/grafana
    # Traffic dashboard: http://server_ip:3000, user/password:admin/admin

### Grafana query
    SELECT "value" FROM "ss" GROUP BY port

## Trigger config update
    curl http://localhost:8000/update  # replace `localhost` to your own remote address

# Panel
This module works without a panel. It just read remote json file and write to influxdb.
But there is a panel existing for management: [https://github.com/fzinfz/tsadmin](https://github.com/fzinfz/tsadmin)
