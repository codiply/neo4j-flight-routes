from __future__ import print_function

import csv
import sys

from py2neo import Graph, Node, Relationship

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

def create_airline_nodes(graph, sourcefile):
    airline_fieldnames = ['id','name','alias','iata','icao','callsign','country','active']
    return create_nodes(graph, 'Airline', sourcefile, airline_fieldnames)

def create_airport_nodes(graph, sourcefile):
    airport_fieldnames = ['id','name','city','country','iata_faa',
                          'icao','latitude','longitude','altitude',
                           'timezone','dst', 'tz_timezone']
    return create_nodes(graph, 'Airport', sourcefile, airport_fieldnames)

def create_route_nodes(graph, sourcefile, airline_nodes, airport_nodes):
    route_fieldnames = ['airline','airline_id','source_airport','source_airport_id',
                        'destination_airport','destination_airport_id', 
                        'codeshare','stops','equipment']
    with open(sourcefile) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=route_fieldnames)
        for row in reader:
            node_properties = {p: row[p] for p in ['codeshare','stops','equipment']}
            route_node = Node('Route', **node_properties)
            graph.create(route_node)
            graph.create(Relationship(route_node, 'FROM', airport_nodes[row['source_airport_id']])) 
            graph.create(Relationship(route_node, 'TO', airport_nodes[row['destination_airport_id']]))
            graph.create(Relationship(route_node, 'OF', airline_nodes[row['airline_id']]))

def main():

    neo4j_uri = 'http://localhost:7474/db/data/'
    
    graph = Graph(neo4j_uri)

    print("Creating airline nodes...")
    airline_nodes = create_airline_nodes(graph, 'data/airlines_cutdown.dat')
    
    print("Creating airport nodes...")
    airport_nodes = create_airport_nodes(graph, 'data/airports_cutdown.dat')
    
    print("Creating route nodes...")
    create_route_nodes(graph, 'data/routes_cutdown.dat', airline_nodes, airport_nodes)  

    return 0

if __name__ == '__main__':
    sys.exit(main())

