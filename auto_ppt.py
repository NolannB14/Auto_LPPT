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


def recursive_search(data, var_to_replaces):
    for element in data:
        if type(data[element]) == dict:
            var_to_replaces = recursive_search(data[element], var_to_replaces)
        else:
            var_to_replaces.append(data[element])
    return var_to_replaces


def replace_all(var_to_replaces):
    for element in var_to_replaces:
        test_file = open("./results/firsttemplate", "r+")
        r_file = test_file.read()
        # Rendre les valeurs affichés plus lisibles
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
    replace_all(var_to_replaces)
    return 0


def main():
    if len(av) != 2 or (len(av) == 2 and av[1] == "-h"):
        usage()
        return 0
    else:
        if find_templates(av[1]) == 84:
            return 84
        shutil.copy("./templates" + av[1], ".")
        generate_template(av[1])
        rename("./" + av[1], "./" + av[1] + ".tex")
        system("pdflatex firsttemplate.tex && find . -type f -not -name 'firsttemplate.pdf' -delete")
    return 0


if __name__ == "__main__":
    exit(main())

# Dernier check à faire pour dynamiser le prog
# Pourquoi pas donner un path en args qui serait l'endroit où l'on met le
# resultat (s'il n'y a pas d'arg alors garder le path par défaut)
