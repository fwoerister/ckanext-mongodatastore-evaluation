#!/bin/bash
set -e

python main.py mongodb

echo "Shut down the current setup and startup the Legacy System. After startup press [Enter] to continue!"
read -r -n 1

python main.py postgresql --nonfunctional 1

echo "Shut down the current setup and startup the New Solution with 4 mongo shards. After startup press [Enter] to continue!"
read -r -n 1

python main.py postgresql --nonfunctional 3 4

echo "Shut down the current setup and startup the New Solution with 5 mongo shards. After startup press [Enter] to continue!"
read -r -n 1

python main.py postgresql --nonfunctional 3 4

echo "Shut down the current setup and startup the New Solution with 6 mongo shards. After startup press [Enter] to continue!"
read -r -n 1

python main.py postgresql --nonfunctional 3 4