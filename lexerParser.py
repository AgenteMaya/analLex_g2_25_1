"""
Maria Eduarda da Fonseca Gonçalves Santos - 2212985
Mayara Ramos Damazio - 2210833
"""

import sys
import pprint

from ply.lex import lex
from ply.yacc import yacc

#lexer
c_code_preamble = [
    """
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

void ligar ( char* namedevice )
{
    printf("%s ligado!\\n", namedevice);
}

void desligar ( char* namedevice )
{
     printf("%s desligado!\\n", namedevice);
}

void alerta ( char* namedevice , char* msg )
{
     printf("%s recebeu o alerta: \\n", namedevice);
     printf ("%s\\n", msg);
}

void alertaComObs ( char* namedevice , char* msg , int var )
{
    printf("%s recebeu o alerta: \\n", namedevice);
    printf ("%s %d\\n", msg, var);
}

int main(void)
{
"""
]

generated_c_code = []

reservados = {
    'ligar'         : 'LIGAR',
    'desligar'      : 'DESLIGAR',
    'enviar'        : 'ENVIAR',
    'alerta'        : 'ALERTA',
    'dispositivo'   : 'DISPOSITIVO',
    'se'            : 'SE',
    'entao'         : 'ENTAO',
    'set'           : 'SET',
    'senao'         : 'SENAO',
    'para'          : 'PARA',
    'todos'         : 'TODOS'
}

tokens = [
    'ID', 'NUM', 'BOOL', 'STRING',
    'OPLOGIC',
    'DOIS_PONTOS', 'VIRGULA', 'PONTO',
    'PARENTESES_I', 'PARENTESES_F',
    'CHAVES_I', 'CHAVES_F',
    'IGUAL', 'AND'
] + list(reservados.values())

t_DOIS_PONTOS   = r':'
t_VIRGULA       = r','
t_PONTO         = r'\.'
t_PARENTESES_I  = r'\('
t_PARENTESES_F  = r'\)'
t_CHAVES_I      = r'{'
t_CHAVES_F      = r'}'
t_IGUAL         = r'='
t_AND           = r'&&'
t_OPLOGIC       = r'>=|<=|==|!=|>|<'

def t_BOOL(t):
    r'True|False'
    t.value = 1 if t.value == 'True' else 0
    return t

def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservados.get(t.value, 'ID') 
    return t

t_ignore = " \t\n" 

def t_error(t):
    print("Caracter ilegal: ", t.value[0])
    t.lexer.skip(1)

lexer = lex(debug=False)

#parser

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
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_device(p):
    '''
    DEVICE : DISPOSITIVO DOIS_PONTOS CHAVES_I COMPONENT_LIST CHAVES_F
    '''
    decls = []
    i=0
    for name in p[4]:
        if not i%2:
            decls.append(f'    char* {name.replace(" ", "_")} = "{name}";')

        else:
            decls.append(f'    float {name.replace(" ", "_")} = 0;')
        i+=1

    p[0] = '\n'.join(decls) + '\n'

def p_component_list(p):
    '''
    COMPONENT_LIST : COMPONENT
                   | COMPONENT_LIST VIRGULA COMPONENT
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_component(p):
    '''
    COMPONENT : ID
              | COMPONENT ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f'{p[1]} {p[2]}'

def p_cmds(p):
    '''
    CMDS : CMDS CMD_TERMINATED
         | CMD_TERMINATED
    '''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]
        
def p_cmd_terminated(p):
    '''
    CMD_TERMINATED : CMD PONTO
    '''
    p[0] = "    " + p[1] + ";\n"

def p_cmd(p):
    '''
    CMD : ATTRIB
        | OBSACT
        | ACT
    '''
    p[0] = p[1]

def p_attrib(p):
    '''
    ATTRIB : SET ID IGUAL VAR
    '''
    p[0] = f'{p[2]} = {p[4]}'

def p_obsact(p):
    '''
    OBSACT : SE OBS ENTAO CMD
           | SE OBS ENTAO CMD SENAO CMD
    '''
    if len(p) == 5:
        p[0] = f'if ({p[2]}) {{\n        {p[4]};\n    }}'
    else:
        p[0] = f'if ({p[2]}) {{\n        {p[4]};\n    }} else {{\n        {p[6]};\n    }}'

def p_obs(p):
    '''
    OBS : ID OPLOGIC VAR
        | ID OPLOGIC VAR AND OBS
    '''
    if len(p) == 4:
        p[0] = f'{p[1]} {p[2]} {p[3]}'
    else:
        p[0] = f'{p[1]} {p[2]} {p[3]} && {p[5]}'

def p_var(p):
    '''
    VAR : NUM
        | BOOL
        | ID
    '''
    p[0] = str(p[1])

def p_act(p):
    '''
    ACT : ACTION ID
        | ENVIAR ALERTA STRING ID
        | ENVIAR ALERTA PARENTESES_I STRING PARENTESES_F ID 
        | ENVIAR ALERTA PARENTESES_I STRING VIRGULA ID PARENTESES_F ID 
        | ENVIAR ALERTA PARENTESES_I STRING PARENTESES_F PARA TODOS DOIS_PONTOS NAMEDEVICELIST
        | ENVIAR ALERTA PARENTESES_I STRING VIRGULA ID PARENTESES_F PARA TODOS DOIS_PONTOS NAMEDEVICELIST
    '''
    if len(p) == 3:
        p[0] = f'{p[1]}({p[2]})'
    elif len(p) == 5:
        p[0] = f'alerta({p[4]}, "{p[3]}")'
    elif len(p) == 7:
        p[0] = f'alerta({p[6]}, "{p[4]}")'
    elif len(p) < 10 and p[5] == ',': 
        p[0] = f'alertaComObs({p[8]}, "{p[4]}", {p[6]})'
    elif len(p) == 10:
        conjuntoStrings = p[9]
        msg = p[4]
        qtdArray = len(conjuntoStrings)
        nomeArray = f"vetorDeDispositivos{p.lineno(1)}"
        stringsDoArray = ", ".join([f'"{d}"' for d in conjuntoStrings])
        p[0] = (
            f'char* {nomeArray}[] = {{ {stringsDoArray} }};\n'
            f'    for (int i = 0; i < {qtdArray}; i++) {{ alerta({nomeArray}[i], "{msg}"); }}'
        )
    else:
        msg = p[4]
        var = p[6]
        conjuntoStrings = p[11]
        qtdArray = len(conjuntoStrings)
        nomeArray = f"vetorDeDispositivos{p.lineno(1)}"
        stringsDoArray = ", ".join([f'"{d}"' for d in conjuntoStrings])
        p[0] = (
            f'char* {nomeArray}[] = {{ {stringsDoArray} }};\n'
            f'    for (int i = 0; i < {qtdArray}; i++) {{ alertaComObs({nomeArray}[i], "{msg}", {var}); }}'
        )

def p_namedevicelist(p):
    '''
    NAMEDEVICELIST : ID
                   | NAMEDEVICELIST VIRGULA ID
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_action(p):
    '''
    ACTION : LIGAR
           | DESLIGAR
    '''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}' (tipo: {p.type}) na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do arquivo!")

parser = yacc(debug=False)

try:
    for i in range(8):
        nameArqObs = 'teste' + str(i+1) + '.ObsAct'
        nameArqC = 'teste' + str(i+1) + '.c'
        with open(nameArqObs, 'r') as arq:
            conteudo = arq.read()
            resultado = parser.parse(conteudo, lexer=lexer)
            if resultado:
                final_c_code = c_code_preamble[0] + resultado + "\n    return 0;\n}\n"
                with open(nameArqC, 'w') as arq_c:
                    arq_c.write(final_c_code)
                print("Arquivo {nameArqC} gerado com sucesso.")
            else:
                print("Não foi possível gerar o código C devido a erros de sintaxe.")

except FileNotFoundError:
    print("Erro: O arquivo {nameArqC} não foi encontrado.")