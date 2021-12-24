#!/usr/bin/env python3


from sys import exit, argv as av
from os import path, makedirs, system, rename
import json
from shutil import copy
import re


def usage():
    try:
        usage_txt = open("usage.txt", "r")
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


def render_folder(filename):
    makedirs("./results")
    copy("./templates/" + filename, "./results")


def recursive_search(data, var_to_replaces):
    for element in data:
        if type(data[element]) == dict:
            var_to_replaces = recursive_search(data[element], var_to_replaces)
        else:
            var_to_replaces.append(data[element])
    return var_to_replaces


def replace_all(var_to_replaces, filename):
    for element in var_to_replaces:
        test_file = open("./results/" + filename, "r+")
        r_file = test_file.read()
        user_input = str(input(element + ":"))
        r_file = re.sub(element, user_input, r_file)
        test_file.seek(0)
        test_file.write(r_file)
        test_file.truncate()
        test_file.close()


def generate_template(path_to_template):
    var_to_replaces = []
    json_f = open("templates/" + path_to_template + ".json")
    data = json.loads(json_f.read())
    data = data["slide_content"]
    for element in data:
        var_to_replaces = recursive_search(element, var_to_replaces)
    replace_all(var_to_replaces, path_to_template)
    return 0


def render(filename):
    rename("./results/" + filename, "./results/" + filename + ".tex")
    system(
        """cd results && pdflatex firsttemplate.tex && 
        find . -type f -not -name 'firsttemplate.pdf' -delete &&
        mv firsttemplate.pdf .. && cd .. && rmdir results"""
    )


def main():
    if len(av) != 2 or (len(av) == 2 and av[1] == "-h"):
        usage()
        return 0
    else:
        try:
            if find_templates(av[1]) == 84:
                return 84
            render_folder(av[1])
            generate_template(av[1])
            render(av[1])
        except KeyboardInterrupt:
            system("rm -r results")
    return 0


if __name__ == "__main__":
    exit(main())
