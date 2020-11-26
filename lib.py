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
        return (struct.pack(">bIII", 0x2, 0, 0, 0) + data)
    elif(type == "DATA"):
        return (struct.pack(">bIII", 0x3, 0, seqnum, fin) + data)
    elif(type=="ANC"):
        return (struct.pack(">bIII", 0x4, 0, 0, 0))

# Split packet to retrieve its meta information
def breakPacket(packet):
    # typ = packet[0]
    # seqnum = int(struct.unpack(">I", packet[5:9])[0])
    # framerate = int(struct.unpack(">I", packet[9:13])[0])
    typ, sampwidth, nchannel, framerate, = struct.unpack(">bIII", packet[:13])

    if(typ == 0x1): 
        frame_count = struct.unpack(">I", packet[13:17])[0]
        filename = packet[17:].decode()
        return "META", [sampwidth, nchannel, framerate, frame_count, filename] 
    elif(typ == 0x2):
        return "SUB", packet[13:]
    elif(typ == 0x3):
        seqnum = nchannel
        if(framerate == 1):
            return "DATA1", [seqnum*1000, packet[13:]]
        else:
            return "DATA", [seqnum*1000, packet[13:]]
    else:
        return "ANC", ""