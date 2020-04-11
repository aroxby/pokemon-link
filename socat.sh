#!/bin/sh
docker-run -p 5738:5738 ubuntu-net-tools socat tcp-listen:5738,fork 'tcp-connect:192.168.56.1:5738!!stdout'