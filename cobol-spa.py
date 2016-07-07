#!/usr/bin/python

# COBOL Static Program Analysis
# cobol-spa (c) 2016 Philip Busch <vzxwco@gmail.com>
# See https://github.com/vzxwco/cobol-spa

import fileinput
import argparse
import sys

TYPE_CONTROL = 'control'
TYPE_DEP = 'dep'


def parse_control(infile):
	"Parse control flow graph."
	for line in infile:
		print (line)

def parse_dep(infile):
	"Parse dependency graph."
	for line in infile:
		print (line)


# Parse command line options
parser = argparse.ArgumentParser(description='COBOL Static Program Analysis')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.2')
parser.add_argument('-t', '--type', choices=[TYPE_CONTROL, TYPE_DEP], required=True, help='Static program analysis type')
parser.add_argument('-i', '--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Input file (default:stdin)')
parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Output file (default:stdout)')
args = parser.parse_args()

# Run parser
if args.type == TYPE_CONTROL:
	json = parse_control(args.infile)
elif args.type == TYPE_DEP:
	json = parse_dep(args.infile)
else:
	pass

# Print result
print (json)


