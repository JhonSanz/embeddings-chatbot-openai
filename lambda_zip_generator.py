import os

def install_dependencies(folder):
    print(f"Copy files for {folder}")
    os.system(f"cp -r {folder} {folder}_copy")
    os.system(f"rm -rf {folder}_copy/__pycache__")
    print(f"Install requirements for {folder}")
    os.system(f"pip install -r requirements.txt -t {folder}_copy")
    print(f"Generate zip file for {folder}")
    os.system(f"cd {folder}_copy && zip -r ../../rafaelpombo_chatbot/{folder}.zip .")
    os.system(f"rm -rf {folder}_copy")


install_dependencies("endpoints/" + "rafaelpombo_chatbot")
