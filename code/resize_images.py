from pathlib import Path
from PIL import Image
curr_dir = Path(".")


def resize_images(directory, w, h):
    """
    :param directory: the path to the folder of images
    :return:
    """
    pathoriginal = curr_dir / directory
    pathresized = curr_dir / (directory + "_resized")
    path_list = pathoriginal.glob("*")
    i = 0
    for c in path_list:
        try:
            im = Image.open(c, "r")
            im = im.resize((w, h), Image.ANTIALIAS)
            im = im.convert("RGB")
            im.save(pathresized / f'{i}.jpg')
            i += 1

        except:
            i += 1
            continue


resize_images('flooding_aerial', 500, 500)
