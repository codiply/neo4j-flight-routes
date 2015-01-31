Data
----------

The `data` folder contains three files with all the data:

- `airlines.dat`
- `airports.dat`
- `routes.dat`

The source of these files is [openflights.org](http://openflights.org/data.html) where you can download their latest versions.
 
The cutdown versions of these files have been created with the script `cutdown_data.py` and contain routes for airports and airlines in the UK only.

Virtualenv
---------

The requirements for running the script `make_graph.py` is just

- py2neo 2.0.4

[Virtualenv](https://virtualenv.pypa.io/en/latest/) is a tool for creating isolated Python environments.

Install the prerequired packages

    sudo apt-get install -y python-virtualenv
    sudo apt-get install -y libpython-dev

Create the bootstrap script

    python create_bootstrap.py

Run the bootstrap script

    python bootstrap.py ENV

Finally, activate the Virtualenv

    source ENV/bin/activate

To deactivate it run
 
    deactivate

Creating the graph
----------

If Neo4j is not running locally you need to change this line in `make_graph.py` accordingly

    neo4j_uri = 'http://localhost:7474/db/data/'

Then simply run

    python make_graph.py

Note that this might take long time to run as I am inserting nodes one by one. For more efficient ways of importing CSV files via cypher have a look [here](http://neo4j.com/docs/stable/cypherdoc-importing-csv-files-with-cypher.html).

