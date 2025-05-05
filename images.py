from PIL import Image

image = Image.open("name.jpg")

# TODO НЕ В РАБОТЕ
new_size = (1260, 500)
resized_image = image.resize(new_size)
resized_image.save("name.jpg")