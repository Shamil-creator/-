import cv2
import numpy as np

def solarization(img, threshold):
    img_float = img.astype(np.float32) / 255
    mask = img_float > threshold
    img_float[mask] = 1 - img_float[mask]
    return (img_float * 255).astype(np.uint8)

def log_contrast(img, c):
    img_float = img.astype(np.float32) / 255
    img_log = c * np.log(1 + img_float)
    return (img_log / img_log.max() * 255).astype(np.uint8)

def main():
    img = cv2.imread('input.jpeg')
    if img is None:
        print("Ошибка: файл input.jpg не найден!")
        return
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    

    print("Выберите метод:")
    print("1 - Соляризация")
    print("2 - Логарифмическое контрастирование")
    
    choice = input("Ваш выбор (1/2): ")

    if choice == '1':
        threshold = float(input("Введите порог (0.1-0.9): "))
        result = solarization(img, threshold)
    elif choice == '2':
        c = float(input("Введите коэффициент C (1-10): "))
        result = log_contrast(img, c)
    else:
        print("Неверный выбор!")
        return
    

    cv2.imwrite('output.jpg', cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
    print("Готово! Результат сохранен как output.jpg")

if __name__ == "__main__":
    main()