#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image


# load pixel
# to csv

class Image2csv:
    def __init__(self, dir, clop_size, dim, colortype, src_image_xy):
        self.dir = dir
        self.clop_size = clop_size
        self.dim = dim
        self.colortype = colortype
        self.src_image_xy = src_image_xy

    def openimages(self):
        file_name = "sea_400x400.jpeg" ##atode edit
        fp = Image.open(file_name)
        src_image = fp.getdata()
        return src_image

    def traindata_create(self, src_image, randum, seed=None):
        """"traindata_create" create training-data for pylearn2 as CSV format.
        """
        if seed == None:
            seed = 1

        if randum == 1:
            pass

        self.clop(src_image, (0,0), self.clop_size)


    def clop(self, src_image, base_point, clop_size):
        cloped = []
        for x in range(base_point[0], clop_size[0]):
            for y in range(base_point[1], clop_size[1]):
                cloped.append(src_image[x])
        print src_image[1]

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
