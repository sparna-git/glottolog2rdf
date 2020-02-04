# Glottolog 2 RDF

This Python script converts the content of the [Glottolog GitHub repository](https://github.com/glottolog), source of the [Glottolog website](https://glottolog.org/) into RDF. It converts parts of the languoid data, and also some metadata about bibliographic references.

This allows to manipulate the data from Glottolog prior to one of its official release. Note that Glottolog offers official RDF releases from its [download page](https://glottolog.org/meta/downloads).

This script does _not_ generate an official Glottolog RDF release. The structure of the output graph differs from the official Glottolog RDF data.


## Tests

Usage : `python -m pytest`
