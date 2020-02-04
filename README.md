# Glottolog 2 RDF

This Python script converts the content of the [Glottolog GitHub repository](https://github.com/glottolog), source of the [Glottolog website](https://glottolog.org/) into RDF. It converts parts of the languoid data, and also some metadata about bibliographic references.

This allows to manipulate the data from Glottolog prior to one of its official release. Note that Glottolog offers official RDF releases from its [download page](https://glottolog.org/meta/downloads).

This script does _not_ generate an official Glottolog RDF release. The structure of the output graph differs from the official Glottolog RDF data.

The script generates an output Turtle file.

## Prerequisites

To run this, you need :
  
  - Python 3 (this has been tested with Python 3.5)
  - Git (to clone Glottolog repository - see below)


## Prerequisites

On Ubuntu, install python-pkd-resources

```
sudo apt install python-pkg-resources
```
  
## Setup the script

1. Get a copy of this script, and `cd` into it :

```
git clone https://github.com/sparna-git/glottolog2rdf.git
cd glottolog2rdf
```

2. Open a new virtual environment and activate it

```
python3.5 -m venv glottolog2rdf-venv
source glottolog2rdf-venv/bin/activate
```

3. Install the dependencies in the virtual environment :

```
pip install -r requirements.txt
```

## Get a copy of Glottolog repository

```
git clone https://github.com/glottolog/glottolog.git
```

The Glottolog repository is ~600Mb.


## Run the Glottolog 2 RDF conversion

The script takes 2 parameters :
  1. Path to source Glottolog repository
  2. Path to output Turtle file
  
To run it, make sure you are in the virtual environment, and run `main.py` with the 2 arguments :

```
python3.5 main.py '/path/to/glottolog' output-full-glottolog.ttl
```

The process takes about 90 minutes to complete, depending on your hardware.

The conversion generates ~ 2.2 million triples.

## Tests

Usage : `python -m pytest`
