#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

class ArgUtils(object):

    def __init__(self):
        pass

    @staticmethod
    def parse_arguments():
        desc = '''
        This is a generic code to handle parameters with the argparse 
        python library. It shows how to use the most useful options of the 
        package.
        '''
        epi = '\tCoded by newlog.\n'
        parser = argparse.ArgumentParser(
            description=desc,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            epilog=epi)
        parser.add_argument(
            'first_mandatory_arg', 
            help='''
            First mandatory argument
            ''',
            type=int)
        parser.add_argument(
            '-a1', '--first_opt_arg',  
            help='''
            First optional argument
            ''', 
            nargs=1,
            default='value1')
        parser.add_argument('--version', 
            action='version', 
            version='%(prog)s 2.0')

        subparsers = parser.add_subparsers(
            help='Several subcommands available')
        new_parser = subparsers.add_parser('subcommand1',
            help='Help for the subcommand1')

        new_parser.add_argument('-a2', '--second_opt_arg',
            help='''
            Second optional argument
            ''', 
            nargs='+')
        new_parser.add_argument('second_mandatory_arg', 
            help='''
            Second mandatory argument
            ''',
            type=str)
        new_parser.add_argument('-v', 
            help='''
            This let's you specify -v, ..., -vvvv..., and 
            you get the number of \'v\'s specified
            ''',
            action='count',
            default=0)
        return parser.parse_args()

if __name__ == "__main__":

    args = ArgUtils.parse_arguments()
    print args
    if args.first_mandatory_arg:
        print("First mand. argument value: %s" % str(args.first_mandatory_arg))
    if args.second_mandatory_arg:
        print("Second mand. argument value: %s" % str(args.second_mandatory_arg))
    if args.first_opt_arg:
        print("First opt. argument value: %s" % str(args.first_opt_arg))
    if args.second_opt_arg:
        print("Second opt. argument value: %s" % str(args.second_opt_arg))
    if args.v:
        print("Verbosity count = %s" % str(args.v))


