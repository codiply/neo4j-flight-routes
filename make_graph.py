from __future__ import print_function

import csv
import sys

from py2neo import Graph, Node

def create_nodes(graph, label, sourcefile, fieldnames):
    with open(sourcefile) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        nodes = {}
        for row in reader:
            node_properties = {p: row[p] for p in fieldnames}
            node = Node(label, **node_properties)
            graph.create(node)
            nodes[row['id']] = node
        return nodes

def main():

    neo4j_uri = 'http://localhost:7474/db/data/'
    
    graph = Graph(neo4j_uri)

    airline_fieldnames = ['id','name','alias','iata','icao','callsign','country','active']
    airline_nodes = create_nodes(graph, 'Airline', 'data/airlines.dat', airline_fieldnames)

    airport_fieldnames = ['id','name','city','country','iata_faa','icao','latitude','longitude','altitude','timezone','dst', 'tz_timezone']
    airport_nodes = create_nodes(graph, 'Airport', 'data/airports.dat', airport_fieldnames)
  
    route_fieldnames = ['airline','airline_id','source_airport','source_airport_id','destination_airport','destionation_airport_id', 'codeshare','stops','equipment']

    return 0

if __name__ == '__main__':
    sys.exit(main())

