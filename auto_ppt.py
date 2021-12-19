#!/usr/bin/env python3


from sys import exit, argv as av
from os import path


def usage():
    try:
        usage_txt = open("usages.txt", "r")
        print(f"{usage_txt.read()}")
    except FileNotFoundError:
        print("Usage : To see the full usage of the file, go on the github repository.")


def find_templates(path_to_template):
    path_to_template = path.join("templates/", path_to_template)
    try:
        template = open(path_to_template, "r")
    except FileNotFoundError:
        print(
            "Wrong template or template not found. To see all available templates go on the github repository."
        )
        return 84
    return 0


def generate_template(path_to_template):
    return 0


def main():
    if len(av) != 2 or (len(av) == 2 and av[1] == "-h"):
        usage()
        return 0
    else:
        if find_templates(av[1]) == 84:
            return 84
        generate_template(av[1])
    return 0


if __name__ == "__main__":
    exit(main())
