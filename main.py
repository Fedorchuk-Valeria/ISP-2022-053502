import argparse
import sys
from handler import Handler
from tests.examples.cls1 import A
from serialization.serializers import *
from serialization.products import *


class Parser:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-f')
        self.parser.add_argument('-mod')
        self.parser.add_argument('-n')
        self.parser.add_argument('-format')
        self.parser.add_argument('-rf')

    def get_arguments(self, arguments: list):
        return self.parser.parse_args(arguments)


if __name__ == '__main__':
    pars = Parser()
    a = JSONClassSerializer.loads(JSONClassSerializer.dumps(Class(A)))
    print(a)
    # args = pars.get_arguments(sys.argv[1:])
    # if args.mod is not None:
    #     Handler.get_serialization(args)
    #     # print('ERROR INPUT')
    # else:
    #     args = pars.get_arguments(sys.argv[1:])
    #     print(args)
