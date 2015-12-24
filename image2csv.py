#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import random
import csv


# load pixel
# to csv

class Image2csv:
    def __init__(self, dir, clip_size, dim, colortype, src_image_xy):
        self.dir = dir
        self.clip_size = clip_size
        self.dim = dim
        self.colortype = colortype
        self.src_image_xy = src_image_xy
        self.scan_xy = (src_image_xy[0] - (clip_size[0] - 1),\
                        src_image_xy[1] - (clip_size[1] - 1))
        self.scan_size = self.scan_xy[0] * self.scan_xy[1]
        self.count = 0

    def openimages(self):
        file_name = "0_sea_400x400.jpeg" ## category_filename.xxx
        category = 0

        fp = Image.open(file_name)
        src_image = fp.getdata()
        return [category, src_image]

    def traindata_create(self, category, src_image, random_flg, seed=None):
        """"traindata_create" create training-data for pylearn2 as CSV format.
        """

        if random_flg == 1:
            if seed == None:
                random.seed(None)
            else:
                print seed
                random.seed(seed)

            readlist = random.sample(xrange(self.scan_size),\
                                            self.scan_size)
        else:
            readlist = xrange(self.scan_size)

        f = open("some.csv", "w")
        writer = csv.writer(f)
        for base_point in readlist:
            tmp = self.clip(category, src_image, base_point, self.clip_size)
            self.pixel_2_csvline(writer, category,tmp)

        f.close()

    def clip(self, category, src_image, base_point, clip_size):
        clipped = []
        for y in range(0, clip_size[1]):
            for x in range(0, clip_size[0]):
                read_point = base_point + x + y * self.src_image_xy[0]
                clipped.append(src_image[read_point])
        return clipped

    def pixel_2_csvline(self, writer, category, image):
        for index, output in enumerate(image):
            if index == 0:
                outline = str(category) + "," + str(output[0])
                for i in range(1, self.dim-1):
                    outline = str(outline) + " " + str(output[i])
            else:
                for i in range(self.dim):
                    outline = str(outline) + " " + str(output[i])
        self.count = self.count + 1
        print self.count
        print outline
        writer.writerow("123")

if __name__ == "__main__":
    I2C=Image2csv("./", (8,8), 3, "rgb", (400,400))
    src = I2C.openimages()
    I2C.traindata_create(src[0], src[1], 1, 1)


#    f = open("some.csv", "wb")
#    writer = csv.writer(f)
#    I2C.pixel_2_csvline(writer, src[0],src[1][0])
#    f.close()
