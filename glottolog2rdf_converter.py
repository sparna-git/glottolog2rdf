# -*- coding: utf-8 -*-
# @Author: Sparna


class Glottolog2RdfConverter():

    def __init__(self, glottolog_dir):
        self.glottolog_dir = glottolog_dir

    def parse_glottolog(self):
        print(self.glottolog_dir)


if __name__ == "__main__":
    cvt = Glottolog2RdfConverter(glottolog_dir='toto')
    cvt.parse_glottolog()
