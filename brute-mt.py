import os
import threading
import subprocess
import argparse
import sys
import shutil
from time import time

# USER: Edit this line to point to your pngcrush executable.
# Remember to escape backslashes if your system uses them.
pngcrush_location = f"D:\\pngcrush_1_8_11_w64.exe"

def run_instance(png_input, instance_num, num_instances, overwrite):
    methods = ["-m %s" % x for x in range(instance_num,151,num_instances)]
    methods = (' '.join(methods)).split(' ')
    temp_folder = png_input + ".temp"
    png_output = os.path.join(temp_folder, os.path.basename(png_input) + "_" + str(instance_num) + ".png")
    cmd = [pngcrush_location, "-nolimits", *methods, png_input, png_output]
    start_time = time()
    subprocess.check_call(cmd, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="PNG input filename")
    parser.add_argument("-t", "--threads", type=int, required=True, help="# of pngcrush instances")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite original PNG")
    args = parser.parse_args()

    png_input = args.input
    png_input = os.path.abspath(png_input)
    num_instances = args.threads
    overwrite = args.overwrite
    
    temp_folder = png_input + ".temp"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    temp_folder = os.path.abspath(temp_folder)

    instances = []
    for i in range(1,num_instances+1):
        instance = threading.Thread(target=run_instance, args=(png_input, i, num_instances, overwrite))
        instance.start()
        instances.append(instance)
    for instance in instances:
        instance.join()

    smallest_file = None
    smallest_size = float("inf")
    for filename in os.listdir(temp_folder):
        path = os.path.join(temp_folder, filename)
        size = os.path.getsize(path)
        if size < smallest_size:
            smallest_file = path
            smallest_size = size

    for filename in os.listdir(temp_folder):
        path = os.path.join(temp_folder, filename)
        if path != smallest_file:
            os.remove(path)
    if overwrite:
        shutil.move(smallest_file, png_input)
    else:
        png_output = os.path.splitext(png_input)[0] + "_brute.png"
        shutil.move(smallest_file, png_output)
    os.rmdir(temp_folder)

if __name__ == "__main__":
    main()
