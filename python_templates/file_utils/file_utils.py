#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ProcessFile(object):

    def __init__(self, filepath):
        if not filepath:
            print("[-] File must be specified.")
            self.inited = False
            return
        if filepath:
            self.inited = True
            self.filepath = filepath

    def read_lines(self):
        if not self.inited:
            print("[-] Class was not correctly created.")
            return
        results = None
        lines = None
        try:
            with open(self.filepath, "r") as f:
                lines = f.readlines()
        except (IOError, OSError) as e:
            print("[-] File could not be read: %s" % e)
        else:
            results = self.__parse(lines)
        return results

    def write_lines(self, lines):
        success = True
        if not self.inited:
            print("[-] Class was not correctly created.")
            return
        if not lines:
            print("[-] You need to specify something to write.")
            return
        try:
            with open(self.filepath, "a") as f:
                f.writelines(lines)
        except (IOError, OSError) as e:
            print("[-] File could not be read: %s" % e)
            success = False
        return success

    def write_binary(self, binary):
        success = True
        if not self.inited:
            print("[-] Class was not correctly created.")
            return
        if not binary:
            print("[-] You need to specify something to write.")
            return
        try:
            with open(self.filepath, "wb") as f:
                f.write(binary)
        except (IOError, OSError) as e:
            print("[-] File could not be read: %s" % e)
            success = False
        return success

    def __parse(self, lines):
        """
        TODO: This functionality is dependant of the use of the class
        """
        if not lines:
            print("[-] No lines to parse specified.")
        return lines


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("[-] Incorrect number of parameters.")
        print("[*] Usage: %s <filepath>" % sys.argv[0])
    else:
        pf = ProcessFile(sys.argv[1])
        lines = pf.read_lines()
        pf = ProcessFile("out.txt")
        pf.write_lines(lines)

