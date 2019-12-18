# -*- coding: utf-8 -*-
# @Author: Sparna

import logging
from pyglottolog import Glottolog
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS


class Glottolog2RdfConverter():

    log = logging.getLogger(__name__)

    def __init__(self, glottolog_dir):
        self.glottolog_dir = glottolog_dir

    def parse_glottolog(self):
        self.log.info("Reading Glottolog from " + self.glottolog_dir)
        glottolog = Glottolog(self.glottolog_dir)
        self.log.info("Glottolog initialized")

        # dictionnaire en comprehension :
        languoids = {l.id: l for l in glottolog.languoids()}
        self.log.info("Languoids dictionnary built successfully")

        # dict(itertools.islice(languoids, 10))
        # languoids = {l.id: l for l in itertools.islice(languoids, 10)}

        # mode normal :
        # languoids = {}
        # for l in glottolog.languoids():
        #    languoids[l.id]=l

        g = Graph()

        self.log.info("Iterating on all Languoids...")
        for l in languoids.values():
            self.log.debug("Processing languoid '"+str(l.id)+"'")
            languoidUri = URIRef("http://glottolog.org/resource/languoid/id/" + str(l.id))
            self.log.debug("Generated languoid URI '"+str(languoidUri)+"'")

            # add the type
            g.add((
                    languoidUri,
                    RDF.type,
                    URIRef("http://purl.org/dc/terms/LinguisticSystem")
            ))

            # add the label
            g.add((
                    languoidUri,
                    RDFS.label,
                    Literal(l.name)
            ))

            # add the parent
            if l.parent is not None:
                parentUri = URIRef("http://glottolog.org/resource/languoid/id/" + str(l.parent.id))
                g.add((
                        languoidUri,
                        SKOS.broader,
                        parentUri
                ))

            # add the references to bib
            for ref in l.sources:
                self.log.debug("Reading ref with bibkey '"+str(ref.bibkey)+"'")
                refObject = ref.get_source(glottolog)
                self.log.debug("Reading ref with glottolog_ref_id '"+str(refObject.fields['glottolog_ref_id'])+"'")
                if refObject.fields['glottolog_ref_id'] is not None:
                    self.log.debug("Referring to glottolog_ref_id '"+str(refObject.fields['glottolog_ref_id'])+"'")
                    bibUri = URIRef("http://glottolog.org/resource/reference/id/"+str(refObject.fields['glottolog_ref_id']))
                    g.add((
                            languoidUri,
                            DCTERMS.description,
                            bibUri
                    ))

                    # self.log.debug(str(refObject.fields))
                    #
                    # # rdf:type
                    # g.add((
                    #     bibUri,
                    #     RDF.type,
                    #     URIRef("http://purl.org/ontology/bibo/Document")
                    # ))
                    #
                    # # title
                    # if('title' in refObject.fields):
                    #     g.add((
                    #         bibUri,
                    #         DCTERMS.title,
                    #         Literal(refObject.fields['title'])
                    #     ))
                    #
                    # # publisher
                    # if('publisher' in refObject.fields):
                    #     g.add((
                    #         bibUri,
                    #         DCTERMS.publisher,
                    #         Literal(refObject.fields['publisher'])
                    #     ))
                    #
                    # # author
                    # if('author' in refObject.fields):
                    #     g.add((
                    #         bibUri,
                    #         DCTERMS.creator,
                    #         Literal(refObject.fields['author'])
                    #     ))
                    #
                    # # year
                    # if('year' in refObject.fields):
                    #     g.add((
                    #         bibUri,
                    #         DCTERMS.created,
                    #         Literal(refObject.fields['year'])
                    #     ))

                else:
                    self.log.warning("Bibkey without glottolog_ref_id '"+str(ref.bibkey)+"'")

        self.log.info("Done iteration on all Languoids")

        self.log.info("Iterating on all References...")
        # Sort all glottolog.bibfiles on priority field

        # sorted_references = sorted(glottolog.bibfiles.items(), key=lambda kv: kv[1])
        self.log.info(str(glottolog.bibfiles))
        sorted_references = sorted(
            glottolog.bibfiles,
            key=lambda bibfile: bibfile.priority,
            reverse=True
        )

        for bibfile in sorted_references:
            self.log.debug(str(bibfile))
            self.log.debug(bibfile.priority)
            # self.log.debug(dir(bibfile))
            # for aRefKey in bibfile.keys():
            #     # self.log.debug(aRefKey)
            #     aReference = bibfile[aRefKey]
            #     # self.log.debug(dir(aReference))
            #     bibUri = URIRef("http://glottolog.org/resource/reference/id/"+str(aReference.fields['glottolog_ref_id']))
            #
            #     # title
            #     if('title' in aReference.fields):
            #         g.add((
            #             bibUri,
            #             DCTERMS.title,
            #             Literal(aReference.fields['title'])
            #         ))

        return g
