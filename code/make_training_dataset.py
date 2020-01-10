from pathlib import Path
import csv
import os

'''
MAKE SURE TO CHANGE METHOD PARAMETERS AS NECCESSARY WHENEVER CHANGING THE DISASTER TYPE. THANKS!!
'''


basic_classes = ['photo_ID', 'disaster?']

classes = ['photo_ID','earthquake', 'flooding', 'fire', 'hurricane', 'bridge', 'building damage', 'lava', 'roads', 'utilities', 'snow', 'vegetation (low)',
           'vegetation (high)', 'river']

# path_to_earthquakes = Path(".") / 'google_images' / 'earthquake_aerial'
# path_to_floods = Path(".") / 'google_images' / 'flooding_aerial'
path_to_hurricanes = Path('.') / 'google_images' / 'hurricane_aerial'
print(path_to_hurricanes.exists())


def path_photos_list(path_to_disaster):
    """
    :param path_to_disaster: self-explanatory
    :return: a list of all the photo paths / directories inside of a folder containing all the photos of a disaster
    of a particular type
    """
    disaster_photos = path_to_disaster.glob('*')

    # try:
    #     photo_list = sorted(disaster_photos, key = lambda x: int(str(x)[str(x).rfind('/') + 1: str(x).rfind('.')]))
    #     print(photo_list)
    #     return photo_list

    # except:
    photo_list = sorted(disaster_photos)
    return photo_list


def rename_files(list_paths, root_path):
    to_ret = []
    """
    :param list_paths: is the list of paths for all the photos in the root_path folder (basically dis_pho_paths)
    :param root_path: is the folder containing all the photos
    """
    count = 0
    for path in list_paths:
        if str(path)[-3:].lower() == 'jpg':
            new_name = convert_num_to_str(count) + '.jpg'
            count += 1
            # try:
            path.replace(root_path / new_name)
            to_ret.append(root_path / new_name)
            # list_paths[i] = root_path / new_name

            # to handle the case where a photo in the format "{insert number here}.jpg" already exists
            # in the original directory:
            # except:
            #     # list_paths[i] = root_path / ('temp' + new_name)
            #     path.rename(root_path / ('temp' + new_name))
            #     path.rename(root_path / new_name)
            #     # list_paths[list_paths.index(path)] = root_path / new_name

        else:
            os.remove(path)

    return to_ret


def convert_num_to_str(num):
    num_str = None
    if 0 <= num < 10:
        num_str = "000" + str(num)
    elif 10 <= num < 100:
        num_str = "00" + str(num)
    elif 100 <= num < 1000:
        num_str = "0" + str(num)
    elif 1000 <= num < 10000:
        num_str = str(num)
    return num_str


# def re_order_images(root_path, path_list):
#     for i in range(len(path_list)):
#         path = path_list[i]
#         num_string = None
#         if 0 <= i < 10:
#             num_string = "000" + str(i)
#         elif 10 <= i < 100:
#             num_string = "00" + str(i)
#         elif 100 <= i < 1000:
#             num_string = "0" + str(i)
#         elif 1000 <= i < 10000:
#             num_string = str(i)
#
#         re_name = root_path / (num_string + '.jpg')
#         path.rename(re_name)
#         path_list[i] = re_name


def make_csv(list_classes, photo_filepaths, dis_type):
    """
    :param list_classes: the labels for all the images
    :param photo_filepaths: self-explanatory
    :param dis_type: short for "disaster type". This variable should be one of the elements in my global "classes"
    variable.
    :return: a .csv file ready for annotations ;). Yay!
    """
    photo_filepaths = sorted(photo_filepaths, key=lambda x: int(str(x)[str(x).rfind('/') + 1: str(x).rfind('.')]))
    with open(f'annotations_{dis_type}.csv', 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames = list_classes)
        writer.writeheader()
        dis_index = list_classes.index(dis_type)

        for file_path in photo_filepaths:
            writer.writerow(set_dict(file_path, dis_index))


def set_dict(fp, index_of_disaster):
    """
    Helper method for writing csv file in the 'make_csv(...)' method right above
    :param fp: filepath
    :return: dictionary in format {class (or label of photo): (binary choice of 0 == False or 1 == True)}
    """
    output_list = [fp] + [0 for _ in range(len(classes) - 1)]
    output_list[index_of_disaster] = 1
    return {classes[i]: output_list[i] for i in range(len(classes))}


dis_pho_paths = path_photos_list(path_to_hurricanes)
dis_pho_paths = rename_files(dis_pho_paths, path_to_hurricanes)
print(len(dis_pho_paths))
# print(dis_pho_paths)
make_csv(classes, dis_pho_paths, 'hurricane')

