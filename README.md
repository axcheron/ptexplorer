# ptexplorer

Convert Packet Tracer files (.pkt/.pka) to XML and vice versa.

[Packet Tracer](https://www.netacad.com/courses/packet-tracer) is a visual simulation tool designed by [Cisco Systems](https://www.cisco.com) that allows users to create network topologies and imitate modern computer networks. The software allows users to simulate the configuration of Cisco routers and switches using a simulated command line interface.

I was kind of curious about the file format used by Packet Tracer. So, after some reverse engineering and analysis here is the result. This tool allow you to convert the *binary* format of the **.pkt/.pka** to a readable **XML** file. 

## Description

The Packet Tracer files (.pkt/.pka) contain the network topology details, configurations and some other information. When you open one of these files, it looks like random binary data :

```text
$ hexdump -C sample.pkt
00000000  23 22 a4 31 67 82 f0 41  70 69 82 d0 c5 e8 fb 4b  |#".1g..Api.....K|
00000010  d2 f9 de a1 0b b4 57 22  a9 20 85 98 4b 1f 04 0f  |......W". ..K...|
00000020  cb 8c b6 4e ea bb d9 e0  08 bc ef d2 76 64 00 0d  |...N........vd..|
00000030  06 55 8a 68 6e ef cc b7  25 8f 0a 25 cd 6f 48 7d  |.U.hn...%..%.oH}|
00000040  7d 0c 78 0e b8 30 00 7c  13 6c 7b 86 bc 48 32 fc  |}.x..0.|.l{..H2.|
00000050  79 34 a5 57 e8 4c b1 6f  f2 64 a7 51 04 a8 66 11  |y4.W.L.o.d.Q..f.|
00000060  d3 d9 63 18 84 29 26 30  bd 7f 1f 5e 6a ec 7b 81  |..c..)&0...^j.{.|
00000070  97 b7 c8 14 72 46 07 4a  c9 30 cc e0 fd 36 90 d7  |....rF.J.0...6..|
00000080  01 39 95 83 57 40 00 31  92 15 68 ba cb 28 aa 01  |.9..W@.1..h..(..|
00000090  5d a9 43 39 bf fa 6f e1  91 e4 6d ae 91 b7 b3 d7  |].C9..o...m.....|
000000a0  1a e8 c3 3a 76 28 b4 4e  33 b9 8e df 9e 10 6e 76  |...:v(.N3.....nv|

[...]
```

I did some reverse engineering on it and discovered that is was in fact a compressed XML file (with [zlib](http://zlib.net/)). However, the compressed file had some kind of encryption. Each byte of the file was xored with the file size as key :

```text
encrypted_byte_0 XOR (file_size - 0) = cleartext_byte_0
encrypted_byte_1 XOR (file_size - 1) = cleartext_byte_1
encrypted_byte_2 XOR (file_size - 2) = cleartext_byte_2
encrypted_byte_3 XOR (file_size - 3) = cleartext_byte_3

[...]
```

So basically, this script simply reverse the XOR and uncompress the file. The result is an XML file :

```xml
<PACKETTRACER5>
 <VERSION>5.2.0.0068</VERSION>
 <NETWORK>
  <DEVICES>
   <DEVICE>
    <ENGINE>
     <TYPE model="1841" >Router</TYPE>
     <NAME translate="true" >Internal</NAME>
     <POWER>true</POWER>
     <DESCRIPTION></DESCRIPTION>
     <MODULE>
      <TYPE>eNonRemovableModule</TYPE>

[...]
```

## Install

Checkout the source: `git clone h`

## Getting Started

```bash
$ python3 ptexplorer.py -h
usage: ptexplorer.py [-h] [-d | -e] infile outfile

Convert Packet Tracer files (.pkt/.pka) to XML and vice versa

positional arguments:
  infile        Packet Tracer file
  outfile       Output file (XML)

optional arguments:
  -h, --help    show this help message and exit
  -d, --decode  convert Packet Tracer file to XML
  -e, --encode  Convert XML to Packet Tracer File

# Decoding
$ python3 ptexplorer.py -d sample.pka sample.xml
[*] Opening Packet Tracer file 'sample.pka'
[*] File size compressed = 164664 bytes
[*] File size uncompressed = 3475692 bytes
[*] Writing XML to 'sample.xml'

# Encoding
$ python3 ptexplorer.py -e sample.xml sample.pkt
[*] Opening XML file 'sample.xml'
[*] File size uncompressed = 3475692 bytes
[*] File size compressed = 164664 bytes
[*] Writing PKT to 'sample.pkt'
```

## License

This project is released under the MIT License. See LICENCE file.