#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import psycopg2
from struct import pack, unpack
from time import sleep
from string import rjust



def sm(c):
    return ":" + c + hex(255 - reduce(operator.xor, map(ord, c)) - 1)[-2:] + "\r\n"


def bin(s):
    s = int(s)
    return str(s) if s <= 1 else bin(s >> 1) + str(s & 1)


def tb(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)


def inv(q):
    w = ""
    i = 0
    for i in range(len(q)):
        w += str(tb(int(q[i]), 0))
        i += 1
    return w


def out(s):
    if s == "0000":
        return 0
    if s == "7D00":
        return 0
    try:
        if int(s, 16) > 2000:
            a = int(inv(bin(int(s, 16) - 1)), 2) / 10.
        else:
            a = int(s, 16) / 10.
    except:
        a = 0
    return a


def sp(s, g):
    r = 0
    q = []
    #    i=0
    while r != len(s):
    #        q['t'+str(i)]=out(s[r:r+g])
        q.append(out(s[r:r + g]))
        r += g
        #        i+=1
    return q


def mes(a, b, n):
    return rjust(hex(a).split("x")[1], 2, "0") + "03" + rjust(hex(b).split("x")[1], 4, "0") + rjust(hex(n).split("x")[1]
                                                                                                    , 4, "0")


def lrc(s):
    i = 0
    hs = ""
    ls = ""
    while i < len(s):
        if i % 2 == 0:
            hs += s[i]
        else:
            ls += s[i]
        i += 1
    i = 0
    h = 0
    l = 0
    while i < len(hs):
        h += int(hs[i], 16)
        l += int(ls[i], 16)
        i += 1
    hi = inv(rjust(bin(h), 4, "0"))
    li = inv(rjust(bin(l), 4, "0"))
    return ":" + s + hex(int(hi, 2))[-1:] + hex(int(li, 2) + 1)[-1:] + "\r\n"

#~ Table of CRC values for high–order byte
auchCRCHi = [
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
    0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
    0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01,
    0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81,
    0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01,
    0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
    0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
    0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01,
    0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
    0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01,
    0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
    0x40]

#~ Table of CRC values for low–order byte
auchCRCLo = [
    0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06, 0x07, 0xC7, 0x05, 0xC5, 0xC4,
    0x04, 0xCC, 0x0C, 0x0D, 0xCD, 0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09,
    0x08, 0xC8, 0xD8, 0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A, 0x1E, 0xDE, 0xDF, 0x1F, 0xDD,
    0x1D, 0x1C, 0xDC, 0x14, 0xD4, 0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3,
    0x11, 0xD1, 0xD0, 0x10, 0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3, 0xF2, 0x32, 0x36, 0xF6, 0xF7,
    0x37, 0xF5, 0x35, 0x34, 0xF4, 0x3C, 0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A,
    0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38, 0x28, 0xE8, 0xE9, 0x29, 0xEB, 0x2B, 0x2A, 0xEA, 0xEE,
    0x2E, 0x2F, 0xEF, 0x2D, 0xED, 0xEC, 0x2C, 0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26,
    0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0, 0x60, 0x61, 0xA1, 0x63, 0xA3, 0xA2,
    0x62, 0x66, 0xA6, 0xA7, 0x67, 0xA5, 0x65, 0x64, 0xA4, 0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F,
    0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68, 0x78, 0xB8, 0xB9, 0x79, 0xBB,
    0x7B, 0x7A, 0xBA, 0xBE, 0x7E, 0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4, 0x74, 0x75, 0xB5,
    0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71, 0x70, 0xB0, 0x50, 0x90, 0x91,
    0x51, 0x93, 0x53, 0x52, 0x92, 0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54, 0x9C, 0x5C,
    0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B, 0x99, 0x59, 0x58, 0x98, 0x88,
    0x48, 0x49, 0x89, 0x4B, 0x8B, 0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C,
    0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42, 0x43, 0x83, 0x41, 0x81, 0x80,
    0x40]
##########################################################################

def crc16 (data):
    uchCRCHi = 0xFF   # high byte of CRC initialized
    uchCRCLo = 0xFF   # low byte of CRC initialized
    uIndex = 0x0000 # will index into CRC lookup table

    for ch in data:
        uIndex = uchCRCLo ^ ord(ch)
        uchCRCLo = uchCRCHi ^ auchCRCHi[uIndex]
        uchCRCHi = auchCRCLo[uIndex]
    return (uchCRCHi << 8 | uchCRCLo)


devices = [21, 22] # Список девайсов
registers = [22, 34] # Список регистров, 22 - влага, 34 - темп

ser = serial.Serial('/dev/ttyAP1') # Ну ты понел
while True: # Бесконечный циклянский
    con = psycopg2.connect(user='django', host='192.168.1.3', database='cpu', password='django')
    cur = con.cursor()
    for id in devices: # Цикл по девайсам
        dvt = {} # Буфер для данных
        for r in registers: # Цикл по регистрам
            w = pack('6B', id, 04, 00, r, 00, 02) # Запрос генерируем
            ser.write(w) # Пишем
            ser.write(pack('=H', crc16(w))) # Дописываем crc16
            sleep(.4) # Засыпаем 200мс
            if ser.inWaiting() != 0: # Если есть хоть один бит в буфере
                sleep(.4) # Если меньше 9 то еще поспать 400mc
                write = ser.read(9)[3:-2][::-1]
                dvt[r] = 0
                dvt[r] = round(unpack('f', write)[0], 3)
            sleep(.2)
            ser.flushInput() # Очищяем
            ser.flushOutput()
#        print dvt
#        print 'INSERT INTO bkz_dvt%s (temp,hmdt,date) VALUES (%s, %s,NOW());' % (id, dvt[34], dvt[22])
        cur.execute('INSERT INTO bkz_dvt%s (temp,hmdt,date) VALUES (%s, %s,NOW());', (id, dvt[34], dvt[22]))
    con.commit()

    ser.write(lrc(mes(1, 0, 24)))
    sleep(.4)
#    print se
    if ser.inWaiting() == 0:
        ser.flushInput()
        ser.flushOutput()
    else:
        data = ser.read(ser.inWaiting())
        a = sp(data[7:-4], 4)
        cur.execute('INSERT INTO bkz_termodat22m (date,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24) VALUES (NOW(),%s);' %  str(a)[1:-1])
        con.commit()
        ser.flushInput()
        ser.flushOutput()
    cur.close()
    con.close()

ser.close() # Зашил порт, по идее ни когда не выполнится.
