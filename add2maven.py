#!/usr/bin/env python

import glob
import zipfile
import StringIO
import os
import sys

DIRECTORY = sys.argv[1]
COMMENT_CHAR= '#'
OPTION_CHAR= '='
COMMAND = "mvn install:install-file -Dfile={0} -DgroupId={1} -DartifactId={2} -Dversion={3} -Dpackaging=jar -DgeneratePom=true"

def parse_config(d):

	buf = StringIO.StringIO(d)
	options = {}
	for line in buf.readlines():

		if COMMENT_CHAR in line:
			line, comment = line.split(COMMENT_CHAR, 1)
		if OPTION_CHAR in line:
			option, value = line.split(OPTION_CHAR, 1)
			option = option.strip()
			value = value.strip()
			options[option] = value

	return options



for name in glob.glob(DIRECTORY + '/*'):
	zf = zipfile.ZipFile(name, "r")
	
	for f in zf.namelist():
		if "pom.properties" in f:
			data = zf.read(f)
			pom = parse_config(data)			

			current_command = COMMAND.format(name, pom['groupId'], pom['artifactId'], pom['version'] )

			os.system(current_command)
		

