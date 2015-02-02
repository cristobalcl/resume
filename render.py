#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""render.py

Generate resume in different formats.
"""

__version__ = "0.0.1"

import sys
import argparse

from pprint import pprint

import yaml
from mako.template import Template


def processCommandLine():
	parser = argparse.ArgumentParser(description="render.py")
	parser.add_argument("-t", "--tmp", metavar="TMP", dest="tmp", type=str, default=".", required=False, help="temporal directory")
	parser.add_argument("-v", "--verbose", action="store_true")
	parser.add_argument("--version", action="version", version="%(prog)s " + __version__)

	return parser.parse_args()


def main():
	args = processCommandLine()

	stream = open("resume.yaml", "r")
	resume = yaml.load(stream)

	if args.verbose: pprint(resume)

	mdTemplate = Template(
				filename="templates/markdown.mako",
				input_encoding="utf-8",
				output_encoding="utf-8",
				encoding_errors="replace"
				)
	with open(args.tmp+"/resume.md", "w") as f:
		f.write(mdTemplate.render(**resume))

	texTemplate = Template(
				filename="templates/hugo.mako",
				input_encoding="utf-8",
				output_encoding="utf-8",
				encoding_errors="replace"
				)
	with open(args.tmp+"/resume.hugo", "w") as f:
		f.write(texTemplate.render(**resume))

	texTemplate = Template(
				filename="templates/latex.mako",
				input_encoding="utf-8",
				output_encoding="utf-8",
				encoding_errors="replace"
				)
	with open(args.tmp+"/resume.tex", "w") as f:
		f.write(texTemplate.render(**resume))

	return 0


if __name__=="__main__":
		sys.exit(main())
