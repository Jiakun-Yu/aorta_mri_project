import csv
import os
import shutil
import cv2

import numpy as np
from PIL import Image as Im
from pydicom import dcmread

# Creating a new path
def create_path(new_path):
    # new_path = 'D:/MRI_project/MRI_png'
    if not os.path.exists(new_path):
        print('triggered')
        os.makedirs(new_path)

def numpy_img_from_dicom_path(dicom_path):
    dicom = dcmread(dicom_path)
    frame = dicom.pixel_array
    window_center = dicom.WindowCenter
    window_width = dicom.WindowWidth
    window_minimum = max(0, window_center - window_width)
    frame = frame - window_minimum
    frame = frame / window_width
    frame = np.clip(frame, 0, 1)
    frame = (frame * 255).astype(np.uint8)
    return frame


# delete folders that are empty
def del_folder_that_are_empty(path):
    for folder in os.listdir(path):
        if folder.endswith('(png)'):
            if not os.listdir(f'{path}/{folder}'):
                os.rmdir(f'{path}/{folder}')

def saving_png_from_dir(path, dst):
    create_path(dst)
    os.chdir(dst)
    for file in os.listdir(path):
        if file.endswith('.dcm'):
           img_instance = numpy_img_from_dicom_path(path+'/'+file)
           image = Im.fromarray(img_instance)
           image.save(f'{dst}/{file}.png','PNG')

'''
# Alternative method using cv2:
img_instance = numpy_img_from_dicom_path('D:\MRI_project\series0001-Body\img0001--2.dcm')
cv2.imshow("image", img_instance)
cv2.imwrite('path.png',img_instance)
cv2.waitKey()
'''

# Move all 'png' files to another file/location
def move_png_to_new_location(path, dst):
    # path = 'D:/MRI_project/MRI_project'
    create_path('D:/MRI_project/MRI_png')
    for file in os.listdir(path):
        if file.endswith('.png'):
            # Move the file to the png_files directory
            shutil.move(path+'/'+file, dst)

# Copy all dicom to a target location
def copy_all_to_another_location(src_folder, dst):
    create_path(dst)
    for folder in os.listdir(src_folder):
        for file in os.listdir(src_folder+'/'+folder):
            src = (src_folder + '/' + folder+'/'+file)
            shutil.copy2(src, dst)

'''
# Get all attributes of DICOM
dir(instance)
'''

'''
# Example of showing PNG image 
path = "D:\MRI_project\MRI_project\series0013-Body\img0001-43.878.dcm"
np_array = numpy_img_from_dicom_path(path)
image = Im.fromarray(np_array)
image.show()
'''

'''
# Categorising all MRI files
path = "D:/MRI_project/MRI_png(all)"
for file in os.listdir(path):
    if file.endswith('.dcm'):
        dfile = dcmread(path+'/'+file)
        dst = f'D:/MRI_project/{dfile.SeriesDescription}'
        create_path(dst)
        shutil.copy2(path+'/'+file,dst)'''

'''
# Categorising DICOM files according to SeriesDescription
path = "D:/MRI_project/MRI_categorised"
for folder in os.listdir(path):
    dst = f'{path}/{folder}(png)'
    create_path(dst)
    for file in os.listdir(f'{path}/{folder}'):
        if file.endswith('.dcm'):
            image_instance = numpy_img_from_dicom_path(f'{path}/{folder}/{file}')
            image = Im.fromarray(image_instance)
            image.save(f'{dst}/{file}.png', 'PNG')
'''

'''
# Move all unreadable dicom files to target location (dst)
path = "D:/MRI_project/MRI_png(all)"
dst = "D:/MRI_project/Unreadable"
create_path(dst)
for file in os.listdir(path):
    if file.endswith('.dcm'):
        try:
            numpy_img_from_dicom_path(path+'/'+file)
        except:
            print('Unable to read dcm file')
            shutil.copy2(f'{path}/{file}', dst)
'''

'''
# Convert aorta_valve_cine_3 DICOM to PNG
path = 'D:/MRI_project/aorta_valve_cine_3'
dst = 'D:/MRI_project/aorta_valve_cine_3(png)'
for file in os.listdir(path):
    if file.endswith('.dcm'):
        dfile = numpy_img_from_dicom_path(path+'/'+file)
        image_instance = Im.fromarray(dfile)
        image_instance.save(f'{dst}/{file}.png', 'PNG')
'''

'''
# Copy src folder to dst
src_folder = 'D:/MRI_project/MRI_project'
dst = 'D:/MRI_project/MRI_png(all)'
copy_all_to_another_location(src_folder, dst)
'''

'''
# Remove all files ending with .png
for file in os.listdir('D:/MRI_project/MRI_png(all)'):
    if file.endswith('.png'):
        os.remove(f'D:/MRI_project/MRI_png(all)/{file}')
'''


'''
# Writing a list of all values from "SeriesDescription" of dicom files
with open('D:/MRI_project/SeriesDescription.csv','w',newline='') as new_csv:
    writer = csv.writer(new_csv)
    writer.writerow(['SeriesDescription'])
    for file in os.listdir('D:/MRI_project/MRI_png(all)'):
        try:
            dicom = dcmread('D:/MRI_project/MRI_png(all)/'+file)
            writer.writerow([dicom.SeriesDescription])
        except:
            pass

# Read the data from the input CSV file (alternative to above)
summary = {}
with open('D:/MRI_project/SeriesDescription.csv', 'r') as input_csv:
    reader = csv.reader(input_csv)
    data = list(reader)
    for row in data:
        for cell in row:
            if cell in summary:
                summary[cell] += 1
            else:
                summary[cell] = 1
'''

'''
# Write the summarized data to the output CSV file
with open('D:/MRI_project/SeriesDescription(Summary).csv', 'w', newline='') as output_csv:
    writer = csv.writer(output_csv)
    for string, count in summary.items():
        writer.writerow([string, count])
'''

# not_aorta = "D:\MRI_project\MRI_project\series0053-Body\img0020--8.58671.dcm"
# aorta = "D:\MRI_project\MRI_project\series0013-Body\img0003-43.878.dcm"
# non_aorta_dicom = dcmread(not_aorta)
# aorta_dicom = dcmread(aorta)
# header = ['CardiacNumberOfImages', 'SequenceVariant', 'SeriesDate', 'SeriesDescription', 'SeriesInstanceUID', 'SeriesNumber', 'SeriesTime', 'SliceLocation', 'SliceThickness', 'SmallestImagePixelValue']
# for x in range(len(header)):
#     print(f'Attribute - {header[x]}: {getattr(non_aorta_dicom,header[x])}')
#     print(f'{header[x]}: {getattr(aorta_dicom,header[x])}')

