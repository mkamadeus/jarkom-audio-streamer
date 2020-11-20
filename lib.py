import struct 

# Untuk tubes 2 modif aja deh jadi packetnya
# type

# Create packet with certain types:
# 0x1 = META
# 0x2 = SUB
# 0x3 = DATA
def createPacket(type, data, fin = 0, seqnum = 0):
    if(type == "META"):
        # print((struct.pack(">bIIII", 0x1, data[0], data[1], data[2], data[3]) + bytes(data[4], 'utf-8')))
        return (struct.pack(">bIIII", 0x1, data[0], data[1], data[2], data[3]) + bytes(data[4], 'utf-8'))
    elif(type == "SUB"):
        return (struct.pack(">bIII", 0x2, 0, 0, 0))
    else:
        return (struct.pack(">bIII", 0x3, 0, seqnum, fin) + data)

# Split packet to retrieve its meta information
def breakPacket(packet):
    typ = packet[0]
    seqnum = struct.unpack(">I", packet[5:9])
    framerate = struct.unpack(">I", packet[9:13])

    if(typ == 0x1): 
        typ, sampwidth, nchannel, framerate, frame_count = struct.unpack(">bIIII", packet[:17])
        filename = packet[17:].decode()
        return "META", [sampwidth, nchannel, framerate, frame_count, filename] 
    elif(typ == 0x2):
        return "SUB", ""
    else:
        if(framerate == 1):
            return "DATA1", (seqnum, packet[13:])
        else:
            return "DATA", (seqnum, packet[13:])