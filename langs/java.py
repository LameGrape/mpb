import glob
import subprocess
import os
from pathlib import Path
import sys
import time
from common import *

def build(buildFile: BuildFile, returnPath = False):
    startTime = time.time()

    cache = {}
    if not os.path.exists("build"): os.mkdir("build")
    if not os.path.exists("build/obj/"): os.mkdir("build/obj/")
    if not os.path.exists("build/.buildcache"): open("build/.buildcache", "w").close()
    with open("build/.buildcache", "r") as file:
        for line in file.readlines():
            split = line.split(":")
            cache[split[0]] = float(split[1])

    javacArgs = []
    if len(buildFile.paths) > 0:
        javacArgs.append("-cp")
        javacArgs.append(f'"{";".join(buildFile.paths)}"')

    files = glob.glob("**/*.java", recursive=True)
    success = True
    for file in files:
        modified = True
        if file in cache.keys():
            modified = os.path.getmtime(file) > cache[file]
        if "-f" in sys.argv or "--force" in sys.argv: modified = True
        if not modified: continue
        if subprocess.run(["javac", file, "-d", "build/obj/"] + javacArgs).returncode == 0:
            cache[file] = os.path.getmtime(file)
        else: success = False
    if success and subprocess.run(["jar", "cf", f"build/{buildFile.name}.jar", "-C", "build/obj/", "."]).returncode == 0:
        print(f"{colors.BOLD}Build success{colors.RESET} -> {colors.MAIN}build/{buildFile.name}.jar{colors.RESET} ({round(time.time() - startTime, 2)} seconds)")
    else:
        print(f"{colors.BOLD}{colors.ERROR}Build failed{colors.RESET} ({round(time.time() - startTime, 2)} seconds)")
        success = False

    with open("build/.buildcache", "w") as file:
        for key, value in cache.items():
            file.write(f"{key}:{value}\n")

    if returnPath: return f"build/{buildFile.name}.jar" if success else None
    return not success

def run(path):
    return subprocess.run(["java", "-jar", path]).returncode

def init(name):
        return f"""[project]
name:{name}
language:java"""