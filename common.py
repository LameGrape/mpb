VERSION = "0.3.7"

class colors:
    MAIN = "\033[38;5;215m"
    ERROR = "\033[31m"
    WARN = "\033[33m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def error(msg): print(f"{colors.ERROR}{msg}{colors.RESET}"); return 1
def warn(msg): print(f"{colors.WARN}{msg}{colors.RESET}")

class BuildFile:
    def __init__(self):
        self.name = "out"
        self.language = "c"
        self.paths = []
        self.libs = []