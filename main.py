# -*- coding: utf-8 -*-
# @Author: Sparna

import sys
import logging
from pyglottolog import Glottolog
from rdflib import Graph, URIRef, term
from rdflib.namespace import RDF
import itertools

# import glottolog2rdf_converter
from glottolog2rdf_converter import Glottolog2RdfConverter as cvt

def main():
    print("Bonjour")


def parse_glottolog(glottolog_dir):

    # logging
    logname='basic.log'

    # logging.basicConfig(filename=logname,
    #                         filemode='a',
    #                         format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    #                         datefmt='%H:%M:%S',
    #                         level=logging.DEBUG)

    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'))  # noqa
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)

    log.info("Reading Glottolog from " + glottolog_dir)
    glottolog = Glottolog(glottolog_dir)
    log.info("Glottolog initialized")

    # dictionnaire en comprehension :
    languoids = {l.id: l for l in glottolog.languoids()}
    log.info("Languoids dictionnary built successfully")

    # dict(itertools.islice(languoids, 10))
    # languoids = {l.id: l for l in itertools.islice(languoids, 10)}

    # mode normal :
    # languoids = {}
    # for l in glottolog.languoids():
    #    languoids[l.id]=l

    g = Graph()

    log.debug("Iterating on all Languoids...")
    for l in languoids.values():
        languoidUri = URIRef("http://glottolog.org/resource/languoid/id/" + l.id)  # noqa
        logging.debug("Processing languoid URI "+languoidUri)

        # add the type
        g.add((
                languoidUri,
                RDF.type,
                URIRef("http://purl.org/dc/terms/LinguisticSystem")
        ))

        # add the label

        # add the parent


    print(g.serialize(destination="output.ttl", format='turtle'))

if __name__ == "__main__":
    # main()
    # print("Hello")
    parse_glottolog('/home/thomas/sparna/00-Clients/MCC/06-OPL/06-Connecteurs/02-Glottolog/glottolog')  # noqa
