import shutil
import os

shutil.copy("sample.txt", "backup_sample.txt")
print("Копия создана.")

if os.path.exists("sample.txt"):
    os.remove("sample.txt")
    print("Оригинал удален.")
