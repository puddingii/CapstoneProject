#! encoding: utf-8

import os
import random

class GeneratePairs:
    """
    Generate the pairs.txt file that is used for training face classifier when calling python `src/train_softmax.py`.
    Or others' python scripts that needs the file of pairs.txt.
    Doc Reference: http://vis-www.cs.umass.edu/lfw/README.txt
    """

    def __init__(self, data_dir, pairs_filepath, img_ext):
        """
        Parameter data_dir, is your data directory.
        Parameter pairs_filepath, where is the pairs.txt that belongs to.
        Parameter img_ext, is the image data extension for all of your image data.
        """
        self.data_dir = data_dir
        self.pairs_filepath = pairs_filepath
        self.img_ext = img_ext


    def generate(self):
        self._generate_matches_pairs()
        self._generate_mismatches_pairs()


    def _generate_matches_pairs(self):
        """
        Generate all matches pairs
        """
        for name in os.listdir(self.data_dir):
            a = []

            for file in os.listdir(self.data_dir + name):
                a.append(file)

            with open(self.pairs_filepath, "a") as f:
                for i in range(3):
                    img_dir = '_'.join(random.choice(a).split('_')[0:-1])
                    l = random.choice(a).split("_")[-1].lstrip("0").rstrip(self.img_ext)
                    r = random.choice(a).split("_")[-1].lstrip("0").rstrip(self.img_ext)
                    print(img_dir, l, r)
                    f.write(img_dir + "\t" + l + "\t" + r + "\n")


    def _generate_mismatches_pairs(self):
        """
        Generate all mismatches pairs
        """
        for i, name in enumerate(os.listdir(self.data_dir)):
            if name == ".DS_Store":
                continue

            print(i, name)
            remaining = os.listdir(self.data_dir)
            remaining = [f_n for f_n in remaining if f_n != ".DS_Store"]
            # del remaining[i] # deletes the file from the list, so that it is not chosen again
            other_dir = random.choice(remaining)

            with open(self.pairs_filepath, "a") as f:
                file1 = random.choice(os.listdir(self.data_dir + name))
                file2 = random.choice(os.listdir(self.data_dir + other_dir))
                #print(file2)
                file2_dir = '_'.join(file2.split('_')[0:-1])
                f.write(name + "\t" + file1.split("_")[-1].lstrip("0").rstrip(self.img_ext) + "\t" + file2_dir + "\t" + file2.split("_")[-1].lstrip("0").rstrip(self.img_ext) + "\t")
                #+ file2_dir + file2.split("_")[-1].lstrip("0").rstrip(self.img_ext)) + "\t
                f.write("\n")


if __name__ == '__main__':
    data_dir = "lfwdata-masked-rename/"
    pairs_filepath = "lfw_masked_pairs.txt"
    img_ext = ".jpg"
    generatePairs = GeneratePairs(data_dir, pairs_filepath, img_ext)
    generatePairs.generate()
