#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import random


# load pixel
# to csv

class Image2csv:
    def __init__(self, dir, clop_size, dim, colortype, src_image_xy):
        self.dir = dir
        self.clop_size = clop_size
        self.dim = dim
        self.colortype = colortype
        self.src_image_xy = src_image_xy
        self.src_image_size = self.src_image_xy[0] * self.src_image_xy[1]

    def openimages(self):
        file_name = "sea_400x400.jpeg" ##atode edit
        fp = Image.open(file_name)
        src_image = fp.getdata()
        return src_image

    def traindata_create(self, src_image, random_flg, seed=None):
        """"traindata_create" create training-data for pylearn2 as CSV format.
        """

        if random_flg == 1:
            if seed == None:
                random.seed(None)
            else:
                print seed
                random.seed(seed)

            readlist = random.sample(xrange(self.src_image_size),\
                                            self.src_image_size)
        else:
            readlist = xrange(self.src_image_size)

        for base_point in readlist:
            self.clop(src_image, base_point, self.clop_size)


    def clop(self, src_image, base_point, clop_size):
        ##print "base_point ", base_point
        cloped = []
        ##print "---start---"
        for y in range(0, clop_size[1]):
            ##print "yyyyy"
            for x in range(0, clop_size[0]):
                read_point = base_point + x + y * self.src_image_xy[0]
                print read_point
                cloped.append(src_image[read_point])
        #print cloped

    def pixel_2_csvline(self):
        print "CSV!"

    def main(self):
        pass
        #src_image =self.openimages()
        #seed = 1
        #self.traindata_create(src_image, 1, seed)

if __name__ == "__main__":
    I2C=Image2csv("./", (8,8), 3, "rgb", (400,300))
    src_image =I2C.openimages()
    I2C.traindata_create(src_image, 1, 1)
