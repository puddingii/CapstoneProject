import os
import sys
from PIL import Image

dataset_path = 'lfwdata-masked'
dataset_new_path = 'lfwdata-masked-rename'
if not os.path.exists(dataset_new_path):
    os.mkdir(dataset_new_path)
for i in os.listdir(dataset_path):
    if not os.path.exists(f'{dataset_new_path}/{i}') :
        os.mkdir(f'{dataset_new_path}/{i}')
image_path = []
image_path_new = []

for i in os.listdir(dataset_path) :
    for j in os.listdir(f'{dataset_path}/{i}'):
        image_path.append(f'{dataset_path}/{i}/{j}')

current_dir = image_path[0].split('/')[1]
cnt = 0
for i in image_path :
    image = Image.open(i)
    img_dir = i.split('/')[1]
    img_name = i.split('/')[-1]
    img_type = i.split('.')[-1]
    
    if not current_dir == img_dir :
        current_dir = img_dir
        cnt = 1
        cnt = str(cnt).zfill(4)
        print(f'{dataset_new_path}/{img_dir}/{img_dir}_{cnt}.{img_type}')
        image.save(f'{dataset_new_path}/{img_dir}/{img_dir}_{cnt}.{img_type}')
        cnt = int(cnt)
    else :
        cnt +=1
        cnt = str(cnt).zfill(4)
        print(f'{dataset_new_path}/{img_dir}/{img_dir}_{cnt}.{img_type}')
        image.save(f'{dataset_new_path}/{img_dir}/{img_dir}_{cnt}.{img_type}')
        cnt = int(cnt)
