from PIL import Image
from pathlib import Path
import os
import csv
from collections import OrderedDict
from tempfile import NamedTemporaryFile
import shutil
def convert2gray(elistabeth):
    for x in range(len(elistabeth)):
        count = 0
        for y in elistabeth[x]:
            count += y
        elistabeth[x] = count/len(elistabeth[x])
    return elistabeth
def reducerange(elistabeth):   # 0-1 range is easier to handle than 0-255
    for x in range(len(elistabeth)):
        elistabeth[x] = round(elistabeth[x]/256, 3)
    return elistabeth

def getpixeldata(filepath):
    im = Image.open(filepath, "r")
    im = list(im.getdata())
    if len(im[0]) == 4:
        temp = []
        for x in im:
            temp.append((x[:3]))
    return im
def removetuples(liz):
    # liz is a list of tuples
    temp = []
    for x in liz:
        for y in x:
            temp.append(y)
    return temp

def resizefolder(foldername, w, h):
    pathoriginal = Path(".") / foldername
    pathresized = Path(".") / (foldername + "_resized")
    os.mkdir(pathresized)
    path_list = pathoriginal.glob("*")
    for c in path_list:
        if str(c)[-3:].lower() == 'jpg' or str(c)[-4:].lower() == 'jpeg':
            try:
                im = Image.open(c, "r")
                im = im.resize((w, h), Image.ANTIALIAS)
                im = im.convert("RGB")
                im.save(pathresized / os.path.basename(c)) # according to some random person on stack overflow, this won't work on a linux machine processing windows paths
            except:
                continue
def main():
    filename = "earthquake_aerial"
    classes = ['photo_ID','earthquake', 'flooding', 'fire', 'hurricane', 'bridge', 'building damage', 'lava', 'roads', 'utilities', 'snow', 'vegetation (low)',
           'vegetation (high)', 'river']
    size_w = 500
    size_h = 500
    classes.extend(list(range(size_w * size_h * 3))) # * 3 is for rgb values
    #resizefolder(filename, size_w, size_h)
    skip = True
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(filename + ".csv", mode='r+') as f, tempfile:
        scribe = csv.DictWriter(tempfile, fieldnames = classes)
        secretary = csv.DictReader(f, fieldnames = classes[:14])
        for row in secretary:
            if skip:
                skip = False
                continue
            photo_ID = row["photo_ID"]


            ######################################################
            im = Image.open(photo_ID, "r")
            im = im.resize((size_w, size_h), Image.ANTIALIAS)
            im = im.convert("RGB")
            info = list(im.getdata())
            if len(info[0]) == 4:
                temp = []
                for x in info:
                    temp.append((x[:3]))
                info = temp
            ######################################################
            # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            #info = getpixeldata(photo_ID) # change to resized photo id until then use above code
            # it does not create a folder of resized images tho
            info = removetuples(info)
            info = reducerange(info)
            pixie = OrderedDict(zip(classes[14:], info))
            row.update(pixie)
            scribe.writerow(row)
    shutil.move(tempfile.name, filename + ".csv")
if __name__ == "__main__":
    main()