# -*- coding: utf-8 -*-
# @Author: Sparna

import sys
import logging
from datetime import datetime, date

# import glottolog2rdf_converter
from glottolog2rdf_converter import Glottolog2RdfConverter


class Main():

    log = logging.getLogger(__name__)

    def __init__(self):
        pass

    def run(self, glottolog_dir):

        # Now
        start_time = datetime.now().time()

        self.log.info("glottolog2rdf starting")

        converter = Glottolog2RdfConverter(glottolog_dir)
        graph = converter.parse_glottolog()

        print(graph.serialize(destination="output.ttl", format='turtle'))
        end_time = datetime.now().time()
        self.log.info(
            "glottolog2rdf executed in " +
            str(datetime.combine(date.min, end_time) -
                datetime.combine(date.min, start_time)))


if __name__ == "__main__":

    # logging
    logname = 'basic.log'
    logging.basicConfig(filename=logname,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',  # noqa
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(
        logging.Formatter(
            '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'))
    out_hdlr.setLevel(logging.DEBUG)
    rootLogger = logging.getLogger(None)
    rootLogger.addHandler(out_hdlr)

    # main()
    # print("Hello")
    main = Main()
    main.run('/home/thomas/sparna/00-Clients/MCC/06-OPL/06-Connecteurs/02-Glottolog/glottolog-single-languoid')  # noqa
