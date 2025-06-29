import sys
import pprint

import ply.yacc as yacc

from lexer import tokens
from lexer import file

def p_programm(p):
    '''
    PROGRAMM : DEVICES CMDS
    '''
    p[0] = p[1] + p[2]

def p_devices(p):
    '''
    DEVICES : DEVICE DEVICE
            | DEVICE DEVICES
    '''

    p[0] = p[1] + p[2]


def p_device(p):
    '''
    DEVICE : dispositivo : {namedevice}
           | dispositivo : {namedevice, observation}
    '''
    if len(p) < 6:
        p[0] = "char* " + p[4] + " = " + p[4] + ";"
    
    else:
        p[0] = "char* " + p[4] + " = " + p[4] + ";\nfloat " + p[6] + " = 0;"


def p_cmds(p):
    '''
    CMDS : ATTRIB
         | OBSACT
         | ACT
    '''
    p[0] = p[1]

def p_attrib(p):
    '''
    ATTRIB : set observation = VAR
    '''
    p[0] = p[2] + " = " + p[4]

def p_obsact(p):
    '''
    OBSACT : SE
           | SES
    '''
    p[0] = p[1]

def p_se(p):
    '''
    SE : se OBS entao ACT
    '''
    p[0] = "if(" + p[2] + ")\n{" + p[4] + ";"

def p_ses(p):
    '''
    SES : se OBS entao ACT senao ACT
    '''
    p[0] = "if(" + p[2] + ")\n{" + p[4] + ";\nelse\n{" + p[6] + ";"

def p_obs(p):
    '''
    OBS : observation oplogic OBSL
    '''
    p[0] = p[1] + p[2]  + p[3]

def p_obsl(p):
    '''
    OBSL : VAR
         | VAR && OBS
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2] + p[3]

def p_var(p):
    '''
    VAR : num bool
    '''
    p[0] = p[1] #TODO

def p_act(p):
    '''
    ACT : ACTION namedevice
        | enviar alerta (msg) namedevice
        | enviar alerta (msg, observation) namedevice
        | enviar alerta (msg, namedevice) para todos namedevices
    '''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    elif len(p) == 6:
        p[0] = "alerta(" + p[6] + p[4] + ");"
    else:
        p[0] = "alertaComObs(" + p[8] + "," + p[4] + "," + p[6] +");"

def p_action(p):
    '''
    ACTION : ligar
           | desligar
    '''
    p[0] = p[1]


parser = yacc.yacc()
#file.write(parser.parse)
file.write("    return 0;\n}\n")
file.close()

