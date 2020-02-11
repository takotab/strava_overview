from configparser import ConfigParser
import pip
import sys

# note: all settings are in settings.ini; edit there, not here
config = ConfigParser(delimiters=["="])
config.read("settings.ini")
cfg = config["DEFAULT"]


def install(package):
    if hasattr(pip, "main"):
        pip._internal.main(["install", package])
    else:
        pip._internal.main(["install", package])


def main():
    with open("req.txt", "w") as f:
        for lib in cfg["requirements"].split(" "):
            f.write(lib + "\n")


if __name__ == "__main__":
    main()
