#!/usr/bin/env python3

import re


def main():
    test_file = open("file1", "r+")
    r_file = test_file.read()
    r_file = re.sub("<test>", "thing", r_file)
    test_file.seek(0)
    test_file.write(r_file)
    test_file.truncate()
    return 0


if __name__ == "__main__":
    exit(main())