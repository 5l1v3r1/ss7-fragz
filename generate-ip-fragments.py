#!/usr/bin/env python2.7

'''
MIT License
Copyright (c) 2019 Orange CERT-CC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from scapy.all import *

def ip_fragment(pkt, fragsize=42):
  assert(IP in pkt)
  for fpkt in fragment(pkt, fragsize=fragsize):
    yield fpkt

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='input filename, expected to a pcap file, containing a single packet containing IP/SCTP/M3UA/SCCP layers')
  parser.add_argument('output', help='output filename')
  args = parser.parse_args()

  pkts = rdpcap(args.input)
  assert(len(pkts) == 1)
  pkt = pkts[0]
  assert(IP in pkt)
  assert(SCTP in pkt)
  assert(SCTPChunkData in pkt)

  pkts = ip_fragment(pkt)

  wrpcap(args.output, pkts)
