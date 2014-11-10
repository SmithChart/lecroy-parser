#!/usr/bin/python

import array
from binascii import *
import struct

def unp_word(data, start):
	"Extracts a word from binary data"
	return int(struct.unpack(">h", data[start:(start+2)])[0])

def unp_long(data, start):
	"Extracts a long from binary data"
	return int(struct.unpack(">i", data[start:(start+4)])[0])

def unp_string(data, start):
	"Reads a String until first nullbyte"
	return data[start:].split("\x00",1)[0]	

def unp_float(data, start):
	"Extracts a float from binary data"
	return float(struct.unpack(">f", data[start:(start+4)])[0])

#Magic Strings
magicHead = 'WF ALL,#'
moreMagic = "WAVEDESC"

myfile = open ("ch1.1", "r")
data=myfile.read()

#Suche Anfang
endOfHead = data.find(magicHead)+ len(magicHead)
data = data[endOfHead:].strip(' ').strip('\r').strip('\n')

hexdata = unhexlify(data)
print "Bytes gelesen: " + str(len(hexdata))

hexdata = hexdata[hexdata.find(moreMagic):]
#print "Magic String: " + repr((hexdata[:50]))

comm_type = unp_word(hexdata, 32)
print "COMM_TYPE:" + str(comm_type)

comm_order = unp_word(hexdata, 34)
print "COMM_ORDER:" + str(comm_order)

WAVE_DESCRIPTOR_len = unp_long(hexdata, 36)
print "WAVE_DESCRIPTOR length: " + str(WAVE_DESCRIPTOR_len)

USER_TEXT_len = unp_long(hexdata, 40)
print "USER_TEXT length:" + str(USER_TEXT_len)

WAVE_ARRAY_1 = unp_long(hexdata, 60)
print "WAVE_ARRAY_1 (Number of bytes for the waveform): " + str(WAVE_ARRAY_1)

print "Instrument name: " + unp_string(hexdata,76)
print "Trace label: " + unp_string(hexdata,96)

HORIZ_INTERVAL = unp_float(hexdata, 176)
print "HORIZ_INTERVAL:" + str(HORIZ_INTERVAL)

TIMEBASE = unp_word(hexdata, 324)
print "TIMEBASE: " + str(TIMEBASE)

VERT_COUPLING = unp_word(hexdata, 326)
print "VERT_COUPLING: " + str(VERT_COUPLING)

FIXED_VERT_GAIN = unp_word(hexdata, 332)
print "FIXED_VERT_GAIN: " + str(FIXED_VERT_GAIN)


VERT_GAIN = unp_float(hexdata, 156)
VERT_OFFSET = unp_float(hexdata, 160)
print "VERT_GAIN / VERT_OFFSET: " + str(VERT_GAIN) + " / " + str(VERT_OFFSET)


#Start of waveform array
i = 346 + USER_TEXT_len
t = 0.
while i<len(hexdata) and i < (346 + USER_TEXT_len + WAVE_ARRAY_1):
	print str(t) + ";" + str(VERT_GAIN * float(unp_word(hexdata,i)) + VERT_OFFSET)
	i += 2
	t += HORIZ_INTERVAL


