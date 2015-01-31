from __future__ import print_function

import csv
import sys

from math import radians, cos, sin, asin, sqrt
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

known_distances = {}

def haversine(lat1, lon1, lat2, lon2): 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1 
 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    r = 6367 # km
    return r * c  

def get_distance(source_airport_node, destination_airport_node):
    s_id, d_id = (source_airport_node.properties['id'], destination_airport_node.properties['id'])
    distance = known_distances.get((s_id, d_id))
    if distance is None:
        lat1 = float(source_airport_node.properties['latitude']) 
        lon1 = float(source_airport_node.properties['longitude'])
        lat2 = float(destination_airport_node.properties['latitude']) 
        lon2 = float(destination_airport_node.properties['longitude'])
        distance = haversine(lat1, lon1, lat2, lon2)
        known_distances[(s_id, d_id)] = distance
        known_distances[(d_id, s_id)] = distance
    return distance

def create_route_nodes(graph, sourcefile, airline_nodes, airport_nodes):
    route_fieldnames = ['airline','airline_id','source_airport','source_airport_id',
                        'destination_airport','destination_airport_id', 
                        'codeshare','stops','equipment']
    with open(sourcefile) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=route_fieldnames)
        for row in reader:
            node_properties = {p: row[p] for p in ['codeshare','stops','equipment']}
            source_airport_node = airport_nodes[row['source_airport_id']]
            destination_airport_node = airport_nodes[row['destination_airport_id']]
            dist = get_distance(source_airport_node, destination_airport_node)
            route_node = Node('Route', distance=dist, **node_properties)
            graph.create(route_node)
            graph.create(Relationship(route_node, 'FROM', source_airport_node)) 
            graph.create(Relationship(route_node, 'TO', destination_airport_node))
            graph.create(Relationship(route_node, 'OF', airline_nodes[row['airline_id']]))

def main():

    neo4j_uri = 'http://localhost:7474/db/data/'
    
    graph = Graph(neo4j_uri)

    print("Creating airline nodes...")
    airline_nodes = create_airline_nodes(graph, 'data/airlines.dat')
    
    print("Creating airport nodes...")
    airport_nodes = create_airport_nodes(graph, 'data/airports.dat')
    
    print("Creating route nodes...")
    create_route_nodes(graph, 'data/routes.dat', airline_nodes, airport_nodes)  

    return 0

if __name__ == '__main__':
    sys.exit(main())

