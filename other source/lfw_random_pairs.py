#! encoding: utf-8
import os
import random
class lfw_Pairs:
    def __init__(self, data_dir, pairs_txt_filepath, img_ext):
        self.data_dir = data_dir
        self.pairs_txt_filepath = pairs_txt_filepath
        self.img_ext = img_ext

    def matches_pairs(self):
        for name in os.listdir(self.data_dir):
            a = []

            for file in os.listdir(self.data_dir + name):
                a.append(file)

            with open(self.pairs_txt_filepath, "a") as f:
                for i in range(3):
                    img_dir = '_'.join(random.choice(a).split('_')[0:-1])
                    #Aaron_Eckhart_0001.jpg
                    l = random.choice(a).split("_")[-1].lstrip("0").rstrip(self.img_ext)
                    r = random.choice(a).split("_")[-1].lstrip("0").rstrip(self.img_ext)
                    print(img_dir, l, r)
                    f.write(img_dir + "\t" + l + "\t" + r + "\n")

    def unmatches_pairs(self):
        for i, name in enumerate(os.listdir(self.data_dir)):

            print(i, name)
            remaining = os.listdir(self.data_dir)
            remaining = [f_n for f_n in remaining if f_n != name]
            other_dir = random.choice(remaining)

            with open(self.pairs_txt_filepath, "a") as f:
                file1 = random.choice(os.listdir(self.data_dir + name))
                file2 = random.choice(os.listdir(self.data_dir + other_dir))
                file2_dir = '_'.join(file2.split('_')[0:-1])
                f.write(name + "\t" + file1.split("_")[-1].lstrip("0").rstrip(self.img_ext) + "\t" +
                        file2_dir + "\t" + file2.split("_")[-1].lstrip("0").rstrip(self.img_ext) + "\t")
                f.write("\n")

if __name__ == '__main__':
    data_dir = "lfwdata-masked-rename/"
    pairs_txt_filepath = "lfw_masked_pairs.txt"
    img_ext = ".jpg"
    Pairs = lfw_Pairs(data_dir, pairs_txt_filepath, img_ext)
    Pairs.matches_pairs()
    Pairs.unmatches_pairs()
