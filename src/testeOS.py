import os
import shutil
from pathlib import Path

# from shutil import copytree
print("ok")
comp = os.path.commonpath(["./classificados/3/3.png", "./classificados/3"])
# ppath = os.path.normpath(os.path.join("./original_deletar/",os.path.dirname("./safe/4/4.png")))
# print(ppath)

# os.makedirs(ppath, exist_ok=True)

# # shutil.move("./safe/5.png","./original_deletar/")
# my_file = Path(ppath)
# if my_file.exists:
#     print(ppath + " already exist. Not going to move.")
# else:
#     shutil.move("./safe/4/4.png",ppath)
    

print(comp)

if comp == "classificados":
    print("????")