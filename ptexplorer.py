#!/usr/bin/python3

""" ptexplorer.py: Convert Packet Tracer files (.pkt/.pka) to XML and vice versa"""

__author__ = 'axcheron'
__license__ = 'MIT License'
__version__ = '0.1'

import argparse
import zlib

def ptfile_decode(infile, outfile):
    with open(infile, 'rb') as f:
        in_data = bytearray(f.read())

    i_size = len(in_data)

    print("[*] Opening Packet Tracer file '%s' " % infile)
    print("[*] File size compressed = %d bytes" % i_size)
    
    out = bytearray()
    # Decrypting each byte with decreasing file length
    for byte in in_data:
        out.append((byte ^ i_size).to_bytes(4, "little")[0])
        i_size = i_size - 1
    
    # The 4 first bytes represent the size of the XML decompressed
    o_size = int.from_bytes(out[:4], byteorder='big')
    print("[*] File size uncompressed = %d bytes" % o_size)

    print("[*] Writing XML to '%s'" % outfile)
    # We decompress the file without the 4 first bytes
    with open(outfile, 'wb') as f:
        f.write(zlib.decompress(out[4:]))

def ptfile_encode(infile, outfile):
    with open(infile, 'rb') as f:
        in_data = bytearray(f.read())

    i_size = len(in_data)

    print("[*] Opening XML file '%s' " % infile)
    print("[*] File size uncompressed = %d bytes" % i_size)

    # Convert uncompressed size to bytes
    i_size = i_size.to_bytes(4, 'big')

    # Compress the file and add the uncompressed size
    out_data = zlib.compress(in_data)
    out_data = i_size + out_data
    o_size = len(out_data)
    print("[*] File size compressed = %d bytes" % o_size)

    xor_out = bytearray()
    # Encrypting each byte with decreasing file length
    for byte in out_data:
        xor_out.append((byte ^ o_size).to_bytes(4, "little")[0])
        o_size = o_size - 1

    print("[*] Writing PKT to '%s'" % outfile)
    # We decompress the file without the 4 first bytes
    with open(outfile, 'wb') as f:
        f.write(xor_out)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Convert Packet Tracer files (.pkt/.pka) to XML and vice versa")

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-d", "--decode", help="Converts Packet Tracer file to XML", action="store_true")
    group.add_argument("-e", "--encode", help="Converts XML to Packet Tracer File", action="store_true")
    parser.add_argument("infile", help="Packet Tracer file", action="store", type=str)
    parser.add_argument("outfile", help="Output file (XML)", action="store", type=str)

    args = parser.parse_args()

    if args.decode:
        ptfile_decode(args.infile, args.outfile)
    elif args.encode:
        ptfile_encode(args.infile, args.outfile)
    else:
        parser.print_help()
        exit(1)
