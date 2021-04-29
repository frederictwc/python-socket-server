import socket
import threading
import time

import logging
import logging.handlers
import os

sem = threading.Semaphore()
serial=0

PACKET_START=0xAC
PACKET_END=0xAD
PACKET_ESCAPE=0xAE
PACKET_ESCAPE_MASK=0x80

class USV:

    def appendByte(self, b, d):
        if (PACKET_START  == b or  PACKET_END  == b or  PACKET_ESCAPE  == b):
            #if ((idx) >= max): return -1;
            d+=  [PACKET_ESCAPE] ;
            #if ((idx) >= max): return -1;
            d+= [b ^  PACKET_ESCAPE_MASK];
        else:
            #if ((idx) >= max): return -1;
            d+= [b];
        return d

    def Protocol_CRC8(self, data, size):
        i = 0;
        j = 0;
        crc = 0;
        #for (i = 0; i < size; ++i)
        for i in range(0,size):
            crc = crc ^ data[i];
            #for (j = 0; j < 8; ++j)
            for j in range(0,8):
                if ((crc & 0x01) != 0):
                    crc = (crc >> 1) ^ 0x8C;
                else:
                    crc >>= 1;
        return crc;

    def Protocol_Pack(self, data):
        size=len(data)
        index = 0;
        ret_len = 0;
        crc = self.Protocol_CRC8(data, size);
        buffer=[PACKET_START];

        for index in range(0, size):
            self.appendByte(data[index], buffer);

        self.appendByte(crc, buffer);

        buffer+=[PACKET_END];
        return buffer;

    def Protocol_UnPack(self, data):
        index = 0;
        pack_len = 0;
        crc = 0;
        buffer=[]
        extra=0

        if(len(data)<=5):
            return [],[]
        while(1):
            if(index+extra>=len(data)):
                break;

            if ((PACKET_ESCAPE != data[index+extra-1]) and (PACKET_END == data[index+extra])):
                break;

            if ((PACKET_START == data[index+extra]) or (PACKET_END == data[index+extra])):
                index+=1
                continue
            if (PACKET_ESCAPE == data[index+extra]):
                extra+=1
                buffer += ([data[index+extra] ^ PACKET_ESCAPE_MASK]);
                pack_len+=1;
                index+=1
                continue
            buffer += [data[index+extra]]
            pack_len+=1
            index+=1



        if (pack_len > 0):
            crc = self.Protocol_CRC8(buffer, pack_len - 1);
            if (crc != buffer[pack_len - 1]):
                return [],[];  #CRC error

        if len(data)-1==index+extra:
            data=[]
        else:
            if(len(data)>index+extra):
                data=data[index+extra+1:]
            else:
                data=[]
        return buffer[:len(buffer)-1], data

class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            print("dskaflj")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("hknhjhdskaflj")
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        self.sock.sendall(msg)

    def myreceive(self):
        self.r=self.sock.recv(1024)
        return self.r

def decode(r):
    if(r[0]==1 and r[1]==0xc):#status
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        spot=r[i]<<8+r[i+1]
        modeOperating=r[i+2]
        taskStatus=r[i+4]
        jobMode=r[i+5]
        print("knknknkn",[hex(no) for no in r])
        logger.info(["knknknkn"]+[hex(no) for no in r])

    elif(r[0]==1 and r[1]==0x0d):#gps
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        lat=r[i]<<56+r[i+1]<<48+r[i+2]<<40+r[i+3]<<32+r[i+4]<<24+r[i+5]<<16+r[i+6]<<8+r[i+7]
        long=r[i+8]<<56+r[i+9]<<48+r[i+10]<<40+r[i+11]<<32+r[i+12]<<24+r[i+13]<<16+r[i+14]<<8+r[i+15]
        print("mflkdngsdan",[hex(no) for no in r])
        logger.info(["mflkdngsdan"]+[hex(no) for no in r])

    elif(r[0]==1 and r[1]==0x0e):#pose
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        direction=r[i]<<24+r[i+1]<<16+r[i+2]<<8+r[i+3]
        vericalShake=r[i+4]<<24+r[i+5]<<16+r[i+6]<<8+r[i+7]
        horizontalShake=r[i+8]<<24+r[i+9]<<16+r[i+10]<<8+r[i+11]
        print("knkknknnn",[hex(no) for no in r])
        logger.info(["knkknknnn"]+[hex(no) for no in r])

    elif(r[0]==1 and r[1]==0x0f):#speed,direction
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        speed=r[i]<<24+r[i+1]<<16+r[i+2]<<8+r[i+3]
        direction=r[i+4]<<24+r[i+5]<<16+r[i+6]<<8+r[i+7]
        print("mkldmflkdngsdan",[hex(no) for no in r])
        logger.info(["mkldmflkdngsdan"]+[hex(no) for no in r])
    elif(r[0]==1 and r[1]==0x10):#vel
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        speed=r[i]<<24+r[i+1]<<16+r[i+2]<<8+r[i+3]
        print("knklnknknn",[hex(no) for no in r])
        logger.info(["knklnknknn"]+[hex(no) for no in r])
    elif(r[0]==1 and r[1]==0x11):#hdt
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        direction=r[i]<<24+r[i+1]<<16+r[i+2]<<8+r[i+3]
        print("ihuiggb",[hex(no) for no in r])
        logger.info(["ihuiggb"]+[hex(no) for no in r])
    elif(r[0]==1 and r[1]==0x12):
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        ele=r[i]
        print("kijfokn",[hex(no) for no in r])
        logger.info(["kijfokn"]+[hex(no) for no in r])
    elif(r[0]==1 and r[1]==0x13):#radar
        print("fkdshfdhsa",[hex(no) for no in r])
        logger.info(["fkdshfdhsa"]+[hex(no) for no in r])
    elif(r[0]==1 and r[1]==0x14):#radar status
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        radarEnable=r[i]
        radar=r[i+1]
        print("khefhfn",[hex(no) for no in r])
        logger.info(["khefhfn"]+[hex(no) for no in r])
    elif(r[0]==1 and r[1]==0x18):#wp info ***
        print("jkbcajdbsbvda",[hex(no) for no in r])
        logger.info(["jkbcajdbsbvda"]+[hex(no) for no in r])
    elif(r[0]==1 and r[1]==0x1B):#bat info#for debug
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        watt=r[i]<<24+r[i+1]<<16+r[i+2]<<8+r[i+3]
        volt=r[i+4]<<24+r[i+5]<<16+r[i+6]<<8+r[i+7]
        current=r[i+8]<<24+r[i+9]<<16+r[i+10]<<8+r[i+11]
        temperature=r[i+12]<<8+r[i+13]
        print("nhorehrgfnv",[hex(no) for no in r])
        logger.info(["nhorehrgfnv"]+[hex(no) for no in r])
    elif(r[0]==1 and r[1]==0x27):#home pos
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        latReturn=r[i]<<56+r[i+1]<<48+r[i+2]<<40+r[i+3]<<32+r[i+4]<<24+r[i+5]<<16+r[i+6]<<8+r[i+7]
        longReturn=r[i+8]<<56+r[i+9]<<48+r[i+10]<<40+r[i+11]<<32+r[i+12]<<24+r[i+13]<<16+r[i+14]<<8+r[i+15]
        print("erhnnnln",[hex(no) for no in r])
        logger.info(["erhnnnln"]+[hex(no) for no in r])
    elif(r[0]==3 and r[1]==0x04):#sample record
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        serialNum=r[i]<<24+r[i+1]<<16+r[i+2]<<8+r[i+3]
        dt=r[i+4]<<24+r[i+5]<<16+r[i+6]<<8+r[i+7]
        lat=r[i+8]<<56+r[i+9]<<48+r[i+10]<<40+r[i+11]<<32+r[i+12]<<24+r[i+13]<<16+r[i+14]<<8+r[i+15]
        long=r[i+16]<<56+r[i+17]<<48+r[i+18]<<40+r[i+19]<<32+r[i+20]<<24+r[i+21]<<16+r[i+22]<<8+r[i+23]
        samplingNum=r[i+24]<<8+r[i+25]
        samplingBottle=r[i+26]
        samplingVol=r[i+27]<<24+r[i+28]<<16+r[i+29]<<8+r[i+30]
        samplingDepth=r[i+31]<<24+r[i+32]<<16+r[i+33]<<8+r[i+34]
        print("ijafee",[hex(no) for no in r])
        logger.info(["ijafee"]+[hex(no) for no in r])
    elif(r[0]==3 and r[1]==0x05):#sampling progress
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        samplingProcess=r[i]
        print("kefkesdjfkka",[hex(no) for no in r])
        logger.info(["kefkesdjfkka"]+[hex(no) for no in r])
    elif(r[0]==3 and r[1]==0x06):#monitor record
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release
        serialNum=r[i]<<24+r[i+1]<<16+r[i+2]<<8+r[i+3]
        dt=r[i+4]<<24+r[i+5]<<16+r[i+6]<<8+r[i+7]
        lat=r[i+8]<<56+r[i+9]<<48+r[i+10]<<40+r[i+11]<<32+r[i+12]<<24+r[i+13]<<16+r[i+14]<<8+r[i+15]
        long=r[i+16]<<56+r[i+17]<<48+r[i+18]<<40+r[i+19]<<32+r[i+20]<<24+r[i+21]<<16+r[i+22]<<8+r[i+23]
        MonitorSpotNum=r[i+24]<<8+r[i+25]
        MonitorNum=r[i+26]
        MonitorID=r[i+27]<<24+r[i+28]<<16+r[i+29]<<8+r[i+30]
        MonitorValue=r[i+31]<<24+r[i+32]<<16+r[i+33]<<8+r[i+34]
        print("jiionknkl",[hex(no) for no in r])
        logger.info(["jiionknkl"]+[hex(no) for no in r])
    elif(r[0]==3 and r[1]==0x07):#monitoring process
        if(r[2]==0):
            i=3
        else:
            i=5
            sem.acquire
            data=[0,0,0,r[4],r[5]]
            buffer=bytearray(usv.Protocol_Pack(data))
            mySocket.mysend(buffer)
            sem.release

        MonitorProcess=r[i]
        print("iuhnjbvg",[hex(no) for no in r])
        logger.info(["iuhnjbvg"]+[hex(no) for no in r])
    else:
        print("fhdkasfiuhnjbvg",[hex(no) for no in r])
        logger.info(["fhdkasfiuhnjbvg"]+[hex(no) for no in r])
