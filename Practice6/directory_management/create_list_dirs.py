import os

os.makedirs("test_dir/sub_dir", exist_ok=True)

print("Список файлов и папок:", os.listdir("."))
