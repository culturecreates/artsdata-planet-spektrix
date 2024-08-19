#!/bin/sh

/opt/ontorefine/dist/bin/ontorefine-cli \
transform /opt/ontorefine/run/terrabrucemajestic.json \
-u http://ontorefine:7333 \
--configurations /opt/ontorefine/run/ontorefine/configuration.json \
-f json >> /opt/ontorefine/run/sample.ttl

exit 0