#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import random
import string
import glob

class Image2CsvTraindata:
    def __init__(self, dir, clip_size, dim, src_image_xy, output_type):
        self.dir = dir
        self.clip_size = clip_size
        self.dim = dim
        self.src_image_xy = src_image_xy
        self.scan_xy = (src_image_xy[0] - (clip_size[0] - 1),\
                        src_image_xy[1] - (clip_size[1] - 1))
        self.scan_size = self.scan_xy[0] * self.scan_xy[1]
        self.output_type = output_type #icml or libsvm
        self.count=0

    def openimages(self, path):
        """"openimages" open images and get category(label).
        Images must be "[Category-number]_xxx.fileformat."
        This function regards prefix as a category.
        """
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
        """"traindata_create" create training-data
            for icml emoption on pylearn2 as CSV format.
        """

        if random_flg == 1:
            if seed == None:
                random.seed(None)
            else:
                print "random seed fixed : %d" %seed
                random.seed(seed)

            readlist = random.sample(xrange(self.scan_size),\
                                            self.scan_size)
        else:
            readlist = xrange(self.scan_size)

        #Create csvfile.
        f = open(output_filename, "w")
        #If icml_train
        if self.output_type == "icml_train":
            f.write("category,pixels\n")

        for base_point in readlist:
            for index in range(len(src_image[0])):
                tmp = self.clip(src_image[0][index], src_image[1][index],\
                                base_point, self.clip_size)
                self.image_2_csvline(f, src_image[0][index],tmp)

        f.close()

    def clip(self, category, src_image, base_point, clip_size):
        clipped = []
        for y in range(0, clip_size[1]):
            for x in range(0, clip_size[0]):
                read_point = base_point + x + y * self.src_image_xy[0]
                clipped.append(src_image[read_point])
        return clipped

    def image_2_csvline(self, writer, category, image):
        """"image_2_scvline" transfer clipped image to csvline.
        """
        #self.count=0
        for index, output in enumerate(image):
            if index == 0:
                if self.output_type == "svm":
                    outline = str(category) + " 1:" + str(output[0])
                elif self.output_type == "icml_train":
                    outline = str(category) + "," + str(output[0])
                else:
                    outline = str(category) + " " + str(output[0])

                #print self.count
                for i in range(1, self.dim):
                    if self.output_type == "svm":
                        outline = str(outline) + " " \
                                + str(i+1) + ":" \
                                + str(output[i])
                    else:
                        outline = str(outline) + " " + str(output[i])
                    self.count = self.count + 1
                    #print self.count
            else:
                for i in range(self.dim):
                    if self.output_type == "svm":
                        outline = str(outline) + " " \
                          + str(i+1+index*self.dim) + ":" \
                          + str(output[i])
                    else:
                        outline = str(outline) + " " + str(output[i])
                    self.count = self.count + 1
                    #print self.count

        outline = str(outline) + "\n"
        writer.write(outline)

if __name__ == "__main__":
    #I2CT=Image2CsvTraindata("./", (8,8), 3, (1300,40), "icml_train")
    I2CT=Image2CsvTraindata("./", (8,8), 3, (1240,40), "icml_test")
    #I2CT=Image2CsvTraindata("./", (8,8), 3, (1300,40), "svm")
    #I2CT=Image2CsvTraindata("./", (8,8), 3, (1240,40), "svm")
    #I2CT=Image2CsvTraindata("./", (1,1), 3, (1240,40), "svm")
    src = I2CT.openimages("[^0-9]*.png")
    #I2CT.traindata_create(src, "train.csv", 1, 1)
    I2CT.traindata_create(src, "test.csv", 1, 1)
    #I2CT.traindata_create(src, "train.txt", 1, 1)
    #I2CT.traindata_create(src, "test_svm3.txt", 1, 1)
    #I2CT.traindata_create(src, "test_svm8.txt", 1, 1)
