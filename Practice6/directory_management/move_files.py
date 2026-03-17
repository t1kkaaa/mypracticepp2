import shutil
import os

open("move_me.txt", "a").close()

shutil.move("move_me.txt", "test_dir/move_me.txt")
print("Файл перемещен в test_dir.")
