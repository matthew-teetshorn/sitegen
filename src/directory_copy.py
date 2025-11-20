import sys
import os
import shutil

DEBUG = False


# Takes an absolute path to src and dest and recursively copies all
# contents from src->dest
# This is an exercise, could also just use 'shutil.copytree()'
def directory_copy_h(src: str, dest: str):
    if not os.path.exists(dest):
        if DEBUG:
            print(f"Creating folder at: {dest}")
        try:
            os.mkdir(dest)
        except Exception as e:
            print(f"Unable to create directory: {dest}")
            print(f"Attempt raised exception: {e}")

    contents = os.listdir(src)
    for item in contents:
        new_src = os.path.join(src, item)
        new_dest = os.path.join(dest, item)
        if os.path.isdir(new_src):
            if DEBUG:
                print(f"Directory found: {new_src}")
            directory_copy_h(new_src, new_dest)
        if os.path.isfile(new_src):
            if DEBUG:
                print(f"File found: {new_src}")
                print(f"Copying file at: {new_src} to {new_dest}")
            shutil.copy(new_src, new_dest)

    return


def directory_copy(src: str, dest: str):
    if not os.path.exists(src):
        raise Exception("Error: Must provide a valid source directory")
    if os.path.exists(dest):
        if DEBUG:
            print(f"Destination directory: {dest} exists")
            ans = input("This will erase the directory, are you sure (Y/n)")

            if ans != "Y":
                print("Shutting down...")
                sys.exit(0)

            print(f"Removing: {dest} and all contents")
        shutil.rmtree(dest)

        directory_copy_h(src, dest)
    return
