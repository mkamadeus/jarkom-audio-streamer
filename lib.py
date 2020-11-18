import struct 

# Untuk tubes 2 modif aja deh jadi packetnya
# type

def createPacket(type, data, fin = 0):
    if(type == "META"):
        return (struct.pack(">bIII", 0x1, data[0], data[1], data[2]))
    elif(type == "SUB"):
        return (struct.pack(">bIII", 0x2, 0, 0, 0))
    else:
        return (struct.pack(">bIII", 0x3, 0, 0, fin) + data)

def breakPacket(packet):
    typ, sampwidth, nchannel, framerate = struct.unpack(">bIII", packet[:13])
    if(typ == 0x1): 
        return "META", [sampwidth, nchannel, framerate]
    elif(typ == 0x2):
        return "SUB", ""
    else:
        if(framerate == 1):
            return "DATA1", packet[13:]
        else:
            return "DATA", packet[13:]


# def createPacket(type, length, seq, data):
#     typ = 0x0
#     if(type == "FIN"):
#         typ = 0x2
#     elif(type == "ACK"):
#         typ = 0x1 
#     elif(type == "FIN-ACK"):
#         typ = 0x3
#     elif(type == "META"):
#         typ = 0x4

#     format_packet = ">bHHH"

#     if(type == "FIN" or type == "DATA" or type == "META"):
#         checksum = calcChecksum(struct.pack(">bHH", typ, length, seq) + data)
#         return (struct.pack(format_packet, typ, length, seq, checksum) + data)
#     elif(type == "ACK" or type == "FIN-ACK"):
#         checksum = calcChecksum(struct.pack(">bHH", typ, 0, seq))
#         return struct.pack(format_packet, typ, 0, seq, checksum)

# def breakPacket(packet):
#     format_packet = ">bHHH"
#     header, data = struct.unpack(format_packet, packet[:7]),  packet[7:]

#     return header, data

    

# var = struct.pack("bH", 1, 322) + data

# header, dat = struct.unpack("bh", var[:4]), var[4:]
# for g in var:
#     print(g)

# packet = createPacket("DATA", len(data), 1, data)

# header, datt = breakPacket(packet)