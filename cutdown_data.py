from __future__ import print_function

import csv
import sys

def cutdown(inputfile, outputfile, fieldnames, predicate, column_to_return=None):
    with open(inputfile) as input, open(outputfile, 'w') as output:
        reader = csv.DictReader(input, fieldnames=fieldnames)
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        s = set()
        for row in reader:
            if predicate(row):
                writer.writerow(row)
                if column_to_return is not None:
                    s.add(row[column_to_return])
        return s
                        
def main():

    country = 'United Kingdom'
    
    airline_fieldnames = ['id','name','alias','iata',
                          'icao','callsign','country','active']
    airline_pred = lambda row: row['country'] == country and row['active'] == 'Y'
    airline_ids = cutdown('data/airlines.dat', 'data/airlines_cutdown.dat', 
                          airline_fieldnames, airline_pred, 'id')

    airport_fieldnames = ['id','name','city','country','iata_faa',
                          'icao','latitude','longitude','altitude',
                          'timezone','dst', 'tz_timezone']
    airport_pred = lambda row: row['country'] == country
    airport_ids = cutdown('data/airports.dat', 'data/airports_cutdown.dat', 
                          airport_fieldnames, airport_pred, 'id')  

    route_fieldnames = ['airline','airline_id','source_airport','source_airport_id',
                        'destination_airport','destination_airport_id', 
                        'codeshare','stops','equipment']
    route_pred = lambda row: (row['airline_id'] in airline_ids and 
                              row['source_airport_id'] in airport_ids and 
                              row['destination_airport_id'] in airport_ids)
    cutdown('data/routes.dat', 'data/routes_cutdown.dat', route_fieldnames, route_pred)

    return 0

if __name__ == '__main__':
    sys.exit(main())
