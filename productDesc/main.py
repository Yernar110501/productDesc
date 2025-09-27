from PIL import Image
import sys

def process_product(image_path: str, model: str, name: str):
    img = Image.open(image_path)
    print(f"Картинка загружена: {img.size}, формат {img.format}")

    print(f"Получены данные: Модель={model}, Название={name}")

    description = f"Описание для {name} ({model}) будет сгенерировано позже."
    category = "Категория будет определена позже."
    return description, category

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Использование: python main.py <image_path> <model> <name>")
        sys.exit(1)

    image_path, model, name = sys.argv[1], sys.argv[2], sys.argv[3]
    desc, cat = process_product(image_path, model, name)

    print("\n--- Результат ---")
    print("Описание:", desc)
    print("Категория:", cat)
