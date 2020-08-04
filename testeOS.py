import os
import shutil
# from shutil import copytree

# comp = os.path.commonpath(["./classificados/3/3.png", "classificados"])
ppath = os.path.normpath(os.path.join("./original_deletar/",os.path.dirname("./safe/4/4.png")))
print(ppath)
# try:
os.makedirs(ppath, exist_ok=True)

# shutil.move("./safe/5.png","./original_deletar/")
shutil.move("./safe/4/4.png",ppath)

# print(comp)

# if comp == "classificados":
#     print("????")