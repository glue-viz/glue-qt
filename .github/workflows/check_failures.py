import os
import sys
from xml.etree import ElementTree

if len(sys.argv) != 2:
    print("Usage: python check_failures.py filename.xml")
    sys.exit(1)

filename = sys.argv[1]

if not os.path.exists(filename):
    print("Output file does not exist, pytest command did not complete")
    sys.exit(1)

et = ElementTree.parse(filename)
results = et.find("testsuite").attrib

if int(results["errors"]) > 0 or int(results["failures"]) > 0:
    print("There were failures/errors as part of the test suite")
    sys.exit(1)
