# -*- coding: utf-8 -*-
# @Author: Sparna

import logging
from datetime import datetime, date
from pyglottolog import Glottolog
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, OWL, XSD


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
        g.bind("bibo", "http://purl.org/ontology/bibo/")
        g.bind("dct", "http://purl.org/dc/terms/")
        g.bind("skos", "http://www.w3.org/2004/02/skos/core#")
        g.bind("owl", "http://www.w3.org/2002/07/owl#")
        g.bind("refid", "http://glottolog.org/resource/reference/id/")
        g.bind("languoid", "http://glottolog.org/resource/languoid/id/")

        countLanguoids = 0
        totalLanguoids = len(languoids.values())
        self.log.info("Iterating on "+str(totalLanguoids)+" Languoids...")
        for l in languoids.values():
            # self.log.debug("Processing languoid '"+str(l.id)+"'")
            languoidUri = URIRef("http://glottolog.org/resource/languoid/id/" + str(l.id))
            # self.log.debug("Generated languoid URI '"+str(languoidUri)+"'")

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

            # add the references to bibliographic key
            for ref in l.sources:
                # in Glottolog, https://glottolog.org/resource/reference/id/hh:g:BerryBerry:Abun redirects
                # to the same page as https://glottolog.org/resource/reference/id/59948
                # do not use bibkey, but key
                biblioUri = URIRef("http://glottolog.org/resource/reference/id/"+str(ref.key))
                g.add((
                        languoidUri,
                        DCTERMS.description,
                        biblioUri
                ))

                # self.log.debug("Reading ref with bibkey '"+str(ref.bibkey)+"'")
                # refObject = ref.get_source(glottolog)
                # self.log.debug("Reading ref with glottolog_ref_id '"+str(refObject.fields['glottolog_ref_id'])+"'")
                # if refObject.fields['glottolog_ref_id'] is not None:
                #     self.log.debug("Referring to glottolog_ref_id '"+str(refObject.fields['glottolog_ref_id'])+"'")
                #     bibUri = URIRef("http://glottolog.org/resource/reference/id/"+str(refObject.fields['glottolog_ref_id']))
                #     g.add((
                #             languoidUri,
                #             DCTERMS.description,
                #             bibUri
                #     ))
                # else:
                #     self.log.warning("Bibkey without glottolog_ref_id '"+str(ref.bibkey)+"'")

            countLanguoids += 1
            if(countLanguoids % 1000 == 0):
                self.log.debug(str(countLanguoids)+"/"+str(totalLanguoids))

        self.log.info("Done iteration on all Languoids")
        self.log.info("Output graph now contains "+str(len(g))+" triples")

        self.log.info("Iterating on all References...")
        # Sort all glottolog.bibfiles on priority field

        # sorted_references = sorted(glottolog.bibfiles.items(), key=lambda kv: kv[1])

        sorted_references = sorted(
            glottolog.bibfiles,
            key=lambda bibfile: bibfile.priority,
            reverse=True
        )

        self.log.info("Will process bibfiles in following order :")
        for bibfile in sorted_references:
            self.log.info(str(bibfile)+" (priority "+str(bibfile.priority)+")")

        for bibfile in sorted_references:
            total = len(bibfile.keys())
            self.log.info("Processing "+str(bibfile)+" with "+str(total)+" entries")
            start_time = datetime.now().time()
            # self.log.debug(dir(bibfile))

            count = 0
            countAlreadyFound = 0
            for aRefKey in bibfile.keys():
                # self.log.debug(aRefKey)
                aReference = bibfile[aRefKey]
                # self.log.debug(dir(aReference))
                bibUri = URIRef("http://glottolog.org/resource/reference/id/"+str(aReference.fields['glottolog_ref_id']))

                if (bibUri, RDF.type, URIRef("http://purl.org/ontology/bibo/Document")) not in g:
                    # rdf:type
                    g.add((
                        bibUri,
                        RDF.type,
                        URIRef("http://purl.org/ontology/bibo/Document")
                    ))

                    # title
                    if('title' in aReference.fields):
                        g.add((
                            bibUri,
                            DCTERMS.title,
                            Literal(aReference.fields['title'])
                        ))

                    # publisher
                    if('publisher' in aReference.fields):
                        g.add((
                            bibUri,
                            DCTERMS.publisher,
                            Literal(aReference.fields['publisher'])
                        ))

                    # author
                    if('author' in aReference.fields):
                        g.add((
                            bibUri,
                            DCTERMS.creator,
                            Literal(aReference.fields['author'])
                        ))

                    # year
                    if('year' in aReference.fields):
                        g.add((
                            bibUri,
                            DCTERMS.created,
                            # Don't use this otherwise we get "1974-01-01"^^xsd:gYear
                            # Literal(aReference.fields['year'], datatype=XSD.gYear)
                            Literal(aReference.fields['year'])
                        ))

                else:
                    countAlreadyFound += 1
                    # self.log.debug(aRefKey+" : ref_id "+aReference.fields['glottolog_ref_id']+" already present, skipping.")

                # always backtrack to ref id with an owl:sameAs
                # concatenate bibfilekey with refid
                g.add((
                    bibUri,
                    OWL.sameAs,
                    URIRef("http://glottolog.org/resource/reference/id/"+str(aRefKey))
                ))

                count += 1
                if(count % 1000 == 0):
                    self.log.debug(str(count)+"/"+str(total))

            end_time = datetime.now().time()
            self.log.info(
                "Done processing " + str(bibfile) + " in " +
                str(
                    datetime.combine(date.min, end_time) -
                    datetime.combine(date.min, start_time)
                )
            )
            self.log.info(str(countAlreadyFound)+" entries were already present (out of "+str(count)+")")

        return g
