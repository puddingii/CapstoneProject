import os
import sys
from PIL import Image

dataset_path = 'data'
dataset_new_path = 'data_21'

if not os.path.exists(dataset_new_path):
    os.mkdir(dataset_new_path)

for i in os.listdir(dataset_path):
    if not os.path.exists(f'{dataset_new_path}/{i}') :
        os.mkdir(f'{dataset_new_path}/{i}')

image_path = []

for i in os.listdir(dataset_path) :
    for j in os.listdir(f'{dataset_path}/{i}'):
        image_path.append(f'{dataset_path}/{i}/{j}')

first_dir = image_path[0].split('/')[1]
current_dir = image_path[0].split('/')[1]
cnt = 0
count = 21
for i in image_path :
    image = Image.open(i)
    img_dir = i.split('/')[1]
    img_name = i.split('/')[-1]
    if not current_dir == img_dir :
        current_dir = img_dir
        cnt = 1
    else :
        cnt +=1
        if not cnt > (count if current_dir == first_dir else count+1 ) :
            image.save(f'{dataset_new_path}/{img_dir}/{img_name}')
print("finish")
