import sys
import pprint

from ply.lex import lex
from ply.yacc import yacc

#file = open("c_file.txt", "w")

#__file__ = 'c_file.c'

c_code = [
    """
    #include <stdio.h>
    #include <stdlib.h>

    void ligar ( char* namedevice )
    {
        printf("%s ligado!\n", namedevice);
    }
    
    void desligar ( char* namedevice )
    {
         printf("%s desligado!\n", namedevice);
    }
    
    void alerta ( char* namedevice , char* msg )
    {
         printf("%s recebeu o alerta: \n", namedevice);
         printf ("%s", msg);
    }
    
    void alertaComObs ( char* namedevice , char* msg , int var )
    {
        printf("%s recebeu o alerta: \n", namedevice);
        printf ("%s %d", msg, var);
    }

    void alertaTodos(char** namedevices, char* msg, int qtd)
    {
        for (int i = 0; i < qtd; i++)
        {
            alerta(namedevices[i], msg);
        }
    }

    int main(void)
    {
        char** vNamedevices [100] [100];

    """
]

reservados = (
    "ligar", "desligar", "enviar_alerta", "dispositivo", "se", "entao", "set", 
    "observation", "senao", "and", "dot", "bool", "num", "namedevice", "namesensor", "para_todos", "dois_pontos",
    "virgula", "parenteses_i", "parenteses_f", "chaves_i", "chaves_f", "igual", "msg", "oplogic"
    )


#expressões regulares dos tokens e constantes
t_ligar         = r'ligar'
t_desligar      = r'desligar'
t_enviar_alerta = r'enviar alerta'
t_dispositivo   = r'dispositivo:'
#t_dispositivos  = r'dispositivos:' acho que isso aqui n existe na gramática, adicionei errado
t_se            = r'se'
t_entao         = r'entao'
t_set           = r'set'
t_observation   = r'[a-zA-Z_]+'
t_senao         = r'senao'
t_and           = r'&&'
t_dot           = r'\.'
t_para_todos    = r'para todos'
t_dois_pontos   = r':'
t_virgula       = r','
t_igual         = r'\='
t_parenteses_i  = r'\('
t_chaves_i      = r'{'
t_parenteses_f  = r'\)'
t_chaves_f      = r'}'
t_msg           = r'[a-zA-Z_]+'

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
    r'[a-zA-Z][a-zA-Z]*'
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

def p_programm(p):
    '''
    PROGRAMM : DEVICES CMDS
    '''
    p[0] = p[1] + p[2]

def p_devices(p):
    '''
    DEVICES : DEVICE DEVICES
            | DEVICE
    '''

    p[0] = p[1] + p[2]


def p_device(p):
    '''
    DEVICE : dispositivo dois_pontos chaves_i namedevice chaves_f
           | dispositivo dois_pontos chaves_i namedevice virgula observation chaves_f
    '''
    if len(p) < 6:
        p[0] = "char* " + p[4] + " = " + p[4] + ";"
    
    else:
        p[0] = "char* " + p[4] + " = " + p[4] + ";\nfloat " + p[6] + " = 0;"

def p_cmds(p):
    '''
    CMDS : CMD dot CMD
         | CMD
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2] + p[3]

def p_cmd(p):
    '''
    CMD : ATTRIB
         | OBSACT
         | ACT
    '''
    p[0] = p[1]

def p_attrib(p):
    '''
    ATTRIB : set observation igual VAR
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
         | VAR and OBS
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
        | enviar_alerta parenteses_i msg parenteses_f namedevice
        | enviar_alerta parenteses_i msg virgula observation parenteses_f namedevice
        | enviar_alerta parenteses_i msg virgula namedevice parenteses_f para_todos namedevices
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


#analisador
parser = yacc(debug=True) # construção do parser

#testando para o arquivo teste1.ObsAct
with open('teste1.ObsAct', 'r') as arq:
    conteudo = arq.read()
    resultado = parser.parse(conteudo, lexer=lexer)
    c_code.append(resultado)
    final_c_code = "\n".join(c_code)

with open('teste1.c', 'w') as arq:
    arq.write(final_c_code)


