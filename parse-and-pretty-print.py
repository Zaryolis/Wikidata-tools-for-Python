import json
import argparse
#------------------------------
# parse-and-pretty-print.py:
# For the wikidata Json dump file, read a single line and pretty-print the Json to a
# more human-friendly, readable form. Most entries are very long, and best inspected with
# your favorite text browsing util (mine is Unix 'less')

# You can get the source data file from https://www.wikidata.org/wiki/Wikidata:Database_download.
#------------------------------
fin = open( '/Volumes/Dumpster/data/wikidata-20240101-all.json', 'rt')
outputFilenameBase = '/Volumes/Dumpster/data/item-%d-output.json'

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--line", type=int)
args = parser.parse_args()

skipToLine = args.line
if skipToLine is None or skipToLine<= 0:
    skipToLine = 5

skip = fin.readline() #Skip the opening bracket
for foo in range(1, skipToLine):
    bar = fin.readline()

line = fin.readline().strip()
if line.endswith(','):
    line = line.strip()[:-1]

obj = json.loads(line)
pretty = json.dumps(obj, indent=4)

outputFilename = outputFilenameBase % skipToLine
fout  = open( outputFilename, "wt" )
fout.write(pretty)
print("Writen to {}".format(outputFilename))

fout.close()