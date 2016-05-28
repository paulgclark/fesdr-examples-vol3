#!/usr/bin/python
# This file reads an input file from gnuradio that contains a 
# digital baseband waveform and prints the bits contained in its 
# payload. The end of the preamble for each transmission is marked
# by gnuradio with a value of 2 or 3. All other values will be 1 or 
# 0.
import io
import sys
from struct import *

payloadLength = 92
waveformFileName = "ook.bin"

# open input file for read access in binary mode
waveformFile = io.open(waveformFileName, 'rb')
# read file contents to a list
waveformData = list(waveformFile.read())
# close the file
waveformFile.close()

# split list based on 2s and 3s, which is where the preamble concludes
segmentList = []
tempSegment = []
for symbolByte in waveformData:
    if (symbolByte == b'\x02') or (symbolByte == b'\x03'):
        # append accumulated segment to list
        segmentList.append(tempSegment)
        # start new temporary segment with the bit underneath the preamble flag
        if symbolByte == b'\x02':
            tempSegment = [b'\x00']
        else:
            tempSegment = [b'\x01']
    else:
        tempSegment.append(symbolByte)

# truncate each list to the size of the payload, 
# eliminating the trailing dead air between transmissions
payloadList = []
for segment in segmentList:
    payload = segment[:payloadLength]
    payloadList.append(payload)

# print payload
for payload in payloadList:
    sys.stdout.write("\n")
    for symbolByte in payload:
        if symbolByte == b'\x01':
            sys.stdout.write("1")
        else:
            sys.stdout.write("0")
    sys.stdout.write("\n")
    
