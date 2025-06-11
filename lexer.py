from ply.lex import lex
from ply.yacc import yacc

file = open("c_file.txt", "w")

file.write(
    """
    #include <stdio.h>
    #include <stdlib.h>
    
    """
)

reservados = {"ligar", "desligar", "enviar alerta", "dispositivo:", "dispositivos:", "se", "entao", "set", "observation", "senao", "&&", "."}

def t_oplogic(t):
    r'<|>|>=|<=|==|!='
    return t

def t_bool(t):
    r'0|1'
    t.value = bool(t.value)
    return t

def t_num(t):
    r'[0-9]+'
    t.value = int(t.value)
    return

def t_namedevice(t):
    r'[a-zA-Z][a-zA-Z]'
    if t.value in reservados:
        t.type = t.value
    return t

def t_namesensor(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reservados: 
        t.type = t.value
    return t