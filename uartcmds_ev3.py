# EV# is master

import json
import ustruct
from pybricks.iodevices import UARTDevice
from pybricks.parameters import Port
#from machine import Pin,I2C
#from compas import *
#import uos
DEBUG=False
uart = UARTDevice(Port.S1,baudrate=115200)

def debug(s):
    if DEBUG:
        print(s)

def disablerepl():
    uos.dupterm(None, 1)

def snd(cmd, value):
        # empty receive buffer
        uart.read_all()
        c={'c':cmd,'v':value}
        cjs=json.dumps(c)
        l=ustruct.pack('<h',len(cjs))
        debug(l+cjs)
        uart.write(l+cjs)

def rcv():
    while (uart.waiting()==0):
        pass
    ls=uart.read(2)
    l=ustruct.unpack('<h',ls)[0]
    debug('rcv %d'%l)
    s=b''
    for i in range(l):
        r=uart.read(1)
        if r!=None:
            s+=r
    debug(s)
    #if uart.any(): # are there any unexpected bytes
    if uart.waiting():
        jnk=uart.read_all()
    try:
        ss=json.loads(s)
    except:
        ss=json.loads({'c':'error','v':'nok'})
    return ss

def sndrcv(cmd,value=None):
    snd(cmd,value)
    return rcv()


def waitcmd():
    a=rcv()
    cmd=a['c']
    val=a['v']
    if cmd in cmds:
        if val!=None:
            r=cmds[cmd](val)
        else:
            r=cmds[cmd]()
        if r!=None:
            snd(cmd,r)
    else:
        snd(cmd,'nok')

def loop():
    while True:
        waitcmd()

def led(v):
    print('led')
    for i in v:
        print(i)
    return 'ok'

def imu():
    return([12.3,11.1,180.0])

def grideye(addr):
    a=[20,21,22,23,24,25,26,27,28]
    return a[addr%9]


def mag():
    x, y, z = mag_sensor.read()                                                                 
    return [x,y,z]   

cmds={'led':led,'imu':imu,'grid':grideye,'mag':mag}   

# init devices
#mag_sensor = HMC5883L(scl=5,sda=4) 

# disable repl on uart
#uos.dupterm(None, 1)
