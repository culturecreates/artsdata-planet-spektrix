#!/bin/bash

# Update the Config file
config_file="ontorefine/configuration.json"
column_additions_file="ontorefine/columns.json"
jq '.operations |= (input + .)' $config_file $column_additions_file > updated-configuration.json

source .venv/bin/activate # activate the virtual environment if applicable
SOURCE=manitobaopera python3 main.py
deactivate

# Start the services in the background
sudo docker compose up -d

# Wait for the server to start
echo "Waiting for server to start..."
while ! curl --output /dev/null --silent --head --fail http://localhost:7333; do
  sleep 5
done
echo "Server started!"

# Send a command to the running container
echo "Running OntoRefine CLI using config.json..."
sudo docker exec onto_refine_spektrix /opt/ontorefine/dist/bin/ontorefine-cli transform ../data/json_data/manitobaopera.json \
  -u http://localhost:7333  \
  --no-clean \
  --configurations ../data/updated-configuration.json  \
  -f json >> entities.ttl

# Open the default browser
open http://localhost:7333

echo "Open Project to edit the RDF Mapping."