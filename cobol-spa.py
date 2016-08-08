#!/usr/bin/python

# COBOL Static Program Analysis
# cobol-spa (c) 2016 Philip Busch <vzxwco@gmail.com>
# See https://github.com/vzxwco/cobol-spa

import fileinput
import argparse
import sys
import re
import json
import pprint

TYPE_CONTROL = 'control'
TYPE_DEP = 'dep'

FORMAT_PYTHON = 'python'
FORMAT_JSON = 'json'
FORMAT_DOT = 'dot'
FORMAT_SQL = 'sql'

def parse_control(infile):
	"Parse control flow graph."
	map = {infile.name: {}}
	section = ''
	re_procdev = re.compile('\s*?PROCEDURE\s*DIVISION\s*?', re.IGNORECASE)
	re_section = re.compile('\s*?(?P<section>\S*)\s*SECTION\s*?\.', re.IGNORECASE)
	re_perform = re.compile('\s*?PERFORM\s*(?P<perform>\S*)', re.IGNORECASE)

	procdev = False
	for line in infile:
		m = re_procdev.match(line)
		if m:
			procdev = True

		if not procdev:
			continue

		m = re_section.match(line)
		if m:
			section = m.group('section')
			map[infile.name].update({section: []})

		m = re_perform.match(line)
		if m:
			perform = m.group('perform')
			if perform.upper() == "VARYING" or perform.upper() == "UNTIL":
				continue
			map[infile.name].update({perform: []})
			map[infile.name][section].append(perform)
	return map

def parse_dep(infile):
	"Parse dependency graph."
	map = {infile.name: []}
	re_module = re.compile('\s*?CALL\s*(?P<module>\S*)', re.IGNORECASE)

	for line in infile:
		m = re_module.match(line)
		if m:
			module = m.group('module')
			map[infile.name].append(module)
	return map

def print_python(outfile, map):
	"Print pythonic."
	pprint.pprint(map, stream=outfile)

def print_json(outfile, map):
	"Print JSON."
	str = json.dumps(map, sort_keys=True, indent=4, separators=(',', ': '))
	print(str, file=outfile)


def print_dot_dict(outfile, obj):
	"Helper function for print_dot()."
	for key in obj:
		print("    \"" + key + "\";", file=outfile)
		for item in obj[key]:
			print("    \"" + key + "\" -> \"" + item + "\";", file=outfile)

def print_dot(outfile, map):
	"Print DOT."
	keys = list(map.keys())
	
	print ("digraph \"" + keys[0] + "\" {", file=outfile)
	print ("\tgraph [splines=ortho, concentrate=true, nodesep=0.8, ranksep=3, pad=5.0];", file=outfile)
	print ('\tnode [shape="box", style="rounded, filled", color="#3366cc", fillcolor="#6699ff", fontname="Arial", fontcolor="white", fontsize="14.0", penwidth = 5];', file=outfile)
	print ('\tedge [color="black", penwidth = 3];\n', file=outfile)

	if type(map[keys[0]]).__name__ == 'dict':
		print_dot_dict(outfile, map[keys[0]])
	else:
		print_dot_dict(outfile, map)

	print ("}", file=outfile)

def print_sql(outfile, map):
	"Print SQL."
	print ("-- Sorry, not implemented yet.")


# Parse command line options
parser = argparse.ArgumentParser(description='COBOL Static Program Analysis')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.2')
parser.add_argument('-t', '--type', choices=[TYPE_CONTROL, TYPE_DEP], required=True, help='Static program analysis type')
parser.add_argument('-f', '--format', choices=[FORMAT_PYTHON, FORMAT_JSON, FORMAT_DOT, FORMAT_SQL], default=FORMAT_PYTHON, help='Output format')
parser.add_argument('-i', '--infile', nargs='?', type=argparse.FileType('r', encoding='UTF-8', errors='ignore'), default=sys.stdin, help='Input file (default:stdin)')
parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w', encoding='UTF-8', errors='ignore'), default=sys.stdout, help='Output file (default:stdout)')
args = parser.parse_args()

# Run parser
if args.type == TYPE_CONTROL:
	map = parse_control(args.infile)
elif args.type == TYPE_DEP:
	map = parse_dep(args.infile)
else:
	pass

# Print result
if args.format == FORMAT_JSON:
	print_json(args.outfile, map)
elif args.format == FORMAT_DOT:
	print_dot(args.outfile, map)
elif args.format == FORMAT_SQL:
	print_sql(args.outfile, map)
else:
	print_python(args.outfile, map)


