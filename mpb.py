import glob
import subprocess
import os
from pathlib import Path
import sys
import time
from common import *
import langs.c as lang_c
import langs.java as lang_java

def help():
    usage = "mpb <command> [args]"
    description = f"""{colors.BOLD}Commands{colors.RESET}:
{colors.MAIN}├─{colors.RESET} help
{colors.MAIN}├─{colors.RESET} build
{colors.MAIN}├─{colors.RESET} run
{colors.MAIN}└─{colors.RESET} init"""
    command = None
    
    if len(sys.argv) > 2:
        command = sys.argv[2]
        valid = False
        if command == "init":
            usage = "mpb init <language>"
            description = f"""Creates a template build file for a specified language in the current directory.
{colors.MAIN}└─{colors.RESET} {colors.BOLD}language{colors.RESET}: The language to use for the template. Not case sensitive. Valid options are as follows:"
   {colors.MAIN}├─{colors.RESET} {colors.BOLD}c{colors.RESET}
   {colors.MAIN}└─{colors.RESET} {colors.BOLD}java{colors.RESET}
"""
            valid = True
        if command == "build":
            usage = "mpb build [args]"
            description = f"""Compiles all files in the project, then collects them all into a single final build.
{colors.MAIN}├─{colors.RESET} {colors.BOLD}-f, --force{colors.RESET}: Force all files to recompile, even ones marked as old in the cache.
{colors.MAIN}└─{colors.RESET} {colors.BOLD}-g, --debug{colors.RESET}: Enable debug mode for supported languages."""
            valid = True
        if command == "run":
            usage = "mpb run [args]"
            description = f"""Builds the project then runs either the built executable, or the run script defined in the build file.
{colors.MAIN}└─{colors.RESET} See {colors.MAIN}mpb help build{colors.RESET} for possible arguments."""
            valid = True
        if command == "help":
            command = None
            valid = True
        if not valid: return error(f"Command not found: {command}")

    print(f"""{colors.BOLD}{colors.MAIN}mappy build tool{colors.RESET} {VERSION}{f' > {colors.BOLD}{command}{colors.RESET}' if command is not None else ''}

{colors.BOLD}Usage{colors.RESET}: {usage}

{description}""")
    return 0

def readBuildFile():
    buildFile = BuildFile()
    currentCategory = ""

    with open("mappy.build") as file:
        for line in file.readlines():
            if (line := line.strip()) == "": continue
            if line.startswith("["):
                currentCategory = line[1:-1]
                continue
            split = [n.strip() for n in line.split(":")]
            match currentCategory:
                case "project":
                    if split[0] == "name": buildFile.name = split[1]
                    if split[0] == "language": buildFile.language = split[1].lower()
                case "include":
                    if split[0] == "lib": buildFile.libs.append(split[1])
                    if split[0] == "path": buildFile.paths.append(split[1])
    return buildFile

def build(returnPath=False):
    if not os.path.exists("mappy.build"): return error("No build file found in directory")
    buildFile = readBuildFile()
    language = buildFile.language
    if language == "c": return lang_c.build(buildFile, returnPath=returnPath)
    if language == "java": return lang_java.build(buildFile, returnPath=returnPath)

def run():
    if not os.path.exists("mappy.build"): return error("No build file found in directory")
    buildFile = readBuildFile()
    language = buildFile.language
    path = build(returnPath=True)
    if path is None: return 1
    if language == "c": return lang_c.run(path)
    if language == "java": return lang_java.run(path)

def init():
    if len(sys.argv) < 3: return error(f"No language specified. See {colors.MAIN}mpb help init{colors.ERROR} for all supported languages")
    if os.path.exists("mappy.build"): return error("Build file already exists in directory")
    language = sys.argv[2].lower()
    name = os.path.basename(os.getcwd())
    
    with open("mappy.build", "w") as file:
        contents = None
        if language == "c": contents = lang_c.init(name)
        if language == "java": contents = lang_java.init(name)
        file.write(contents)
    print(f"Wrote build file to {colors.MAIN}mappy.build{colors.RESET}")

def main():
    if len(sys.argv) == 1: return help()
    match sys.argv[1]:
        case "help": return help()
        case "build": return build()
        case "run": return run()
        case "init": return init()
        case _: return help()

if __name__ == "__main__": sys.exit(main())