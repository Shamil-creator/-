from PIL import Image, ImageEnhance
import numpy as np

def solarize(image, threshold=128):
    image_np = np.array(image)
    image_np[image_np > threshold] = 255 - image_np[image_np > threshold]
    return Image.fromarray(image_np)


def LogarithmicContrast(image, c=255):
    image_np = np.array(image).astype(np.float32)
    image_np = c * np.log(1 + image_np) / np.log(1 + c)
    image_np = np.uint8(np.clip(image_np, 0, 255))
    return Image.fromarray(image_np)


def process_image(input_image_path, output_image_path, method='solarize', threshold=128, c=255, quality=95, format='JPEG'):
    image = Image.open(input_image_path)

    if method == 'solarize':
        result_image = solarize(image, threshold)
    elif method == 'logarithmic':
        result_image = LogarithmicContrast(image, c)
    else:
        print("Неизвестный метод")
        exit()

    result_image.save(output_image_path, format=format, quality=quality)
    print("Изображения сохранены")


input_path = 'input.jpeg'
output_path_solarize = 'solarized.jpg'
output_path_log = 'logarithmed.jpg'

process_image(input_path, output_path_solarize, method='solarize', threshold=150)

process_image(input_path, output_path_log, method='logarithmic', c=255)

