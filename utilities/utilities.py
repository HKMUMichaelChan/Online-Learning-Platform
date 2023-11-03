import os
from PIL import Image


def create_blank_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass

# 示例
# file_path = "path/to/your/file.txt"
# create_blank_file(file_path)


def crop_to_square(image_path):

    image = Image.open(image_path)


    width, height = image.size


    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size


    cropped_image = image.crop((left, top, right, bottom))

    cropped_image.save(image_path)


# 示例
# image_path = "path/to/your/image.jpg"
# crop_to_square(image_path)
