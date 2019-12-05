#!/usr/bin/python3
# -*- coding: utf-8 -*-

from glottolog2rdf_converter import Glottolog2RdfConverter


def test_parse_glottolog():
    cvt = Glottolog2RdfConverter(
        glottolog_dir='samples/glottolog-single-languoid/')
    cvt.parse_glottolog()
    assert True
