#!/bin/bash

read -p "This will delete all data in /var/lib/neo4j/data folder. Are you sure (y/n)? " -n 1 -r
echo

sudo rm -rf /var/lib/neo4j/data/*
sudo service neo4j-service restart
