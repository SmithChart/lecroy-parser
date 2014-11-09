#!/usr/bin/python

import array
from binascii import *

#Magic Strings
magicHead = 'WF ALL,#'

myfile = open ("ch1.1", "r")
data=myfile.read()

#Suche Anfang
endOfHead = data.find(magicHead)+ len(magicHead)
print "Start index: " + str(endOfHead)
data = data[endOfHead:].strip(' ').strip('\r').strip('\n')

print "String len" + str(len(data))

print data[:5]
hexdata = unhexlify(data)

print "Bytes gelesen: " + str(len(hexdata))

print "Magic String: " + b2a_uu(hexdata[:8])
