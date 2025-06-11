from ply.lex import lex
from ply.yacc import yacc

file = open("c_file.txt", "w")

__file__ = 'lexer.c'

file.write(
    """
    #include <stdio.h>
    #include <stdlib.h>
    
    """
)

reservados = (
    "ligar", "desligar", "enviar_alerta", "dispositivo", "dispositivos", "se", "entao", "set", 
    "observation", "senao", "and", "dot", "oplogic", "bool", "num", "namedevice", "namesensor"
    )


#expressões regulares dos tokens e constantes
t_ligar         = r'ligar'
t_desligar      = r'desligar'
t_enviar_alerta = r'enviar alerta'
t_dispositivo   = r'dispositivo:'
t_dispositivos  = r'dispositivos:'
t_se            = r'se'
t_entao         = r'entao'
t_set           = r'set'
t_observation   = r'observation'
t_senao         = r'senao'
t_and           = r'&&'
t_dot           = r'\.'

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

t_ignore = " \t\n" #ignorar whitespaces

def t_error(t):
    print("Caracter ilegal: ", t.value[0])

tokens = reservados #precisa de uma lista de tokens para rodar

lexer = lex(debug=True)