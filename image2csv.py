#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import random
import string
import glob

class Image2csv:
    def __init__(self, dir, clip_size, dim, colortype, src_image_xy):
        self.dir = dir
        self.clip_size = clip_size
        self.dim = dim
        self.colortype = colortype # not implemented.
        self.src_image_xy = src_image_xy
        self.scan_xy = (src_image_xy[0] - (clip_size[0] - 1),\
                        src_image_xy[1] - (clip_size[1] - 1))
        self.scan_size = self.scan_xy[0] * self.scan_xy[1]

    def openimages(self, path):
        open_files = glob.glob(path)
        category = []
        src_image = []

        for file_name in open_files:
            fp = Image.open(file_name)
            tmp = string.split(file_name, "_")
            category.append(tmp[0])
            src_image.append(fp.getdata())
        return [category, src_image]

    def traindata_create(self, src_image, output_filename,\
                         random_flg, seed=None):
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

        f = open(output_filename, "w")
        index =0
        for base_point in readlist:
            for index in range(len(src_image[0])):
                tmp = self.clip(src_image[0][index], src_image[1][index],\
                                base_point, self.clip_size)
                self.pixel_2_csvline(f, src_image[0][index],tmp)

        f.close()

    def clip(self, category, src_image, base_point, clip_size):
        clipped = []
        for y in range(0, clip_size[1]):
            for x in range(0, clip_size[0]):
                read_point = base_point + x + y * self.src_image_xy[0]
                clipped.append(src_image[read_point])
        return clipped

    def pixel_2_csvline(self, writer, category, image):
        print category
        for index, output in enumerate(image):
            if index == 0:
                outline = str(category) + "," + str(output[0])
                for i in range(1, self.dim-1):
                    outline = str(outline) + " " + str(output[i])
            else:
                for i in range(self.dim):
                    outline = str(outline) + " " + str(output[i])
        outline = str(outline) + "\n"
        writer.write(outline)


if __name__ == "__main__":
    I2C=Image2csv("./", (8,8), 3, "rgb", (400,400))
    src = I2C.openimages("[^0-9]*.jpeg")
    I2C.traindata_create(src, "train.csv", 1, 1)
