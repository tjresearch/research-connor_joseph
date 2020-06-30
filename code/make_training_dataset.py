from pathlib import Path
import csv

basic_classes = ['photo_ID', 'disaster_type']
classes = ['photo_ID','disaster_type', 'bridge', 'damaged', 'lava', 'roads', 'utilities', 'snow', 'vegetation (low)',
           'vegetation (high)', 'building', 'flooding', 'river', 'useful', 'smoke']

path_to_earthquakes = Path(".") / 'google_images' / 'earthquake'
print(path_to_earthquakes.exists())
earthquake_photos = path_to_earthquakes.glob('*')

photo_list = sorted(earthquake_photos)


def make_csv(list_classes, data):
    with open('annotations.csv', 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames = classes)
        writer.writeheader()
        for file_path in photo_list:
            temp_dict = set_dict(file_path)
            writer.writerow(temp_dict)


def set_dict(fp):
    # run through nn or something using filepath

    # disaster type key:     {0:none, 1:"earthquake"}

    output_list = [fp, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return {classes[i]: output_list[i] for i in range(len(classes))}




