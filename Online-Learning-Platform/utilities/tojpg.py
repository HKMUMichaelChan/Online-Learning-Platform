from PIL import Image

def convert_png_to_jpg(png_file, jpg_path):
    # 打开 PNG 图像
    image = Image.open(png_file)

    # 将图像转换为 RGB 模式（如果是 RGBA 模式）
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # 保存为 JPEG 格式
    image.save(jpg_path, 'JPEG')

# # 调用函数进行转换
# convert_png_to_jpg('input.png', 'output.jpg')