# -*- coding: utf-8 -*-
# @Author: Sparna

import logging
from pyglottolog import Glottolog
from rdflib import Graph, URIRef, term
from rdflib.namespace import RDF


class Glottolog2RdfConverter():

    log = logging.getLogger(__name__)

    def __init__(self, glottolog_dir):
        self.glottolog_dir = glottolog_dir

    def parse_glottolog(self):
        print(self.glottolog_dir)

        self.log.info("Reading Glottolog from " + self.glottolog_dir)
        glottolog = Glottolog(self.glottolog_dir)
        self.log.info("Glottolog initialized")

        # dictionnaire en comprehension :
        languoids = {l.id: l for l in glottolog.languoids()}
        self.log.info("Languoids dictionnary built successfully")

        # dict(itertools.islice(languoids, 10))
        # languoids = {l.id: l for l in itertools.islice(languoids, 10)}

        # mode normal :
        # languoids = {}
        # for l in glottolog.languoids():
        #    languoids[l.id]=l

        g = Graph()

        self.log.debug("Iterating on all Languoids...")
        for l in languoids.values():
            languoidUri = URIRef("http://glottolog.org/resource/languoid/id/" + l.id)  # noqa
            self.log.debug("Processing languoid URI "+languoidUri)

            # add the type
            g.add((
                    languoidUri,
                    RDF.type,
                    URIRef("http://purl.org/dc/terms/LinguisticSystem")
            ))

            # add the label

            # add the parent

        return g

if __name__ == "__main__":
    cvt = Glottolog2RdfConverter(glottolog_dir='toto')
    cvt.parse_glottolog()
