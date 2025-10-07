import sys
import time
import json
import traceback
from typing import Any

#------------------------------
# extract-label-desc.py:
# For the wikidata Json dump file, read out only the label, description, and id properties
# of that very long file(see https://www.wikidata.org/wiki/Wikidata:Database_download).
# It gives you a smaller, more readable slice of sheer volume of data that is stored there, but
# may not be very useful beyond that.
#
# Note that I'm skipping over the items with a label of 'Template:' or
# a description of 'Wikimedia disambiguation page', as I didn't think they added much of any relevance
# to the output.
#
# Some base stats from the run
#   CPU: M2 Pro for a mac mini
#   Runtime: 4h 17m for "en"
#   Lines: 106.9M
#   Output size: 11G
#------------------------------
# Enter your paths and locale
locale = 'EN'
fin =  open( '/Volumes/Dumpster/data/wikidata-20240101-all.json', 'rt')
fout = open('/Volumes/Dumpster/data/label-desc-{}.json'.format(locale), "wt")

printInterval = 1000000
lcLocale = locale.lower() #All locales in data file are lower case

skip = fin.readline() #Read the opening '['
fout.write(skip)      #Write as start of output file

count       = 1
processed   = 0
lastLine    = False
nextline    = None
startTime = time.time()
#------------------------------------------
def countIncrementAndPrint():
    global count, fout
    count += 1
    if count % printInterval == 0:
        print('Completed %12s lines' % f"{count:,}")
        fout.flush() #so we can see partial results as it runs

def nextValidLine():
    global fin
    while True:
        line = fin.readline()
        countIncrementAndPrint()
        outJson: dict[Any, Any] = {}
        outLine = ''

        if line.startswith("]"):
            return line
        clean = line.strip()    #Remove the line break
        if clean.endswith(","): #Remove trailing comma
            clean = clean[:-1]
        try:
            pyObj = json.loads(clean) #Load into Python object
        except:
            print ("Parse error on line %s" % f"{count:,}")
            print( "Error text: '%s'" % clean)
            traceback.print_exc(file=sys.stdout)
            quit()
        try:
            labelObj = dict(pyObj['labels'])
            outJson["label"] = labelObj[lcLocale]["value"]
            descObj = dict(pyObj['descriptions']) #Assume that if there's a label, there's a desc
            outJson["description"] = descObj[lcLocale]["value"]
            if outJson['label'].startswith('Template:') or outJson['description'].startswith("Wikimedia disambiguation page"):
                continue
            outJson['id'] = pyObj['id'] #All items have this
        except KeyError: #Catch the case when there is no key for that locale. Sometimes I miss Perl :(
            continue
        try:
            outLine = json.dumps(outJson)
        except: #Anything bad, exit
            print ("Error on line %s" % f"{count:,}")
            print( "Error text:\n'" + f"{outJson}" + "'")
            traceback.print_exc(file=sys.stdout)
            quit()
        return outLine

#------------------------------------------
#       Begin main
print("Begin run at: %s, for locale '%s'" % (time.ctime(startTime), locale))
firstLine = nextValidLine()
nextLine = nextValidLine()
while True:
    if nextLine.startswith(']'):
        fout.write(firstLine + '\n]\n')
        break
    else:
        fout.write(firstLine + ',\n')
    processed += 1
    firstLine = nextLine
    nextLine = nextValidLine()

countIncrementAndPrint()
print("Read %12s lines total" % f"{count:,}")
print("Processed %12s lines for locale '%s" % (f"{processed:,}", locale) )
print("Run start at: %s" % time.ctime(startTime))
print("Run end at: %s" % time.ctime(time.time()))

fout.close()
fin.close()