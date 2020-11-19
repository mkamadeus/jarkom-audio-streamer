import struct 

# Untuk tubes 2 modif aja deh jadi packetnya
# type

# Create packet with certain types:
# 0x1 = META
# 0x2 = SUB
# 0x3 = DATA
def createPacket(type, data, fin = 0):
    if(type == "META"):
        return (struct.pack(">bIII", 0x1, data[0], data[1], data[2]))
    elif(type == "SUB"):
        return (struct.pack(">bIII", 0x2, 0, 0, 0))
    else:
        return (struct.pack(">bIII", 0x3, 0, 0, fin) + data)

# Split packet to retrieve its meta information
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