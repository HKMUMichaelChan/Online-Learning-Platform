from PIL import Image

def convert_png_to_jpg(png_file, jpg_path):
    # 打開 PNG 圖像
    image = Image.open(png_file)

    # 將影像轉換為 RGB 模式（如果是 RGBA 模式）
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # 儲存為 JPEG 格式
    image.save(jpg_path, 'JPEG')

