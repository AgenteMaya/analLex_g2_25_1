import sys
import pprint

from ply.lex import lex
from ply.yacc import yacc

# Código base em C que será gerado, incluindo a função 'alertaTodos'
c_code_preamble = [
    """
#include <stdio.h>
#include <stdlib.h>

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

void alertaTodos(char* namedevices[], char* msg, int qtd)
{
    for (int i = 0; i < qtd; i++)
    {
        alerta(namedevices[i], msg);
    }
}

int main(void)
{
"""
]

# Lista para armazenar o código C gerado a partir dos comandos
generated_c_code = []

# Palavras reservadas e tokens
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
    'DOIS_PONTOS', 'VIRGULA', 'DOT',
    'PARENTESES_I', 'PARENTESES_F',
    'CHAVES_I', 'CHAVES_F',
    'IGUAL', 'AND'
] + list(reservados.values())


# Expressões regulares dos tokens
t_DOIS_PONTOS   = r':'
t_VIRGULA       = r','
t_DOT           = r'\.'
t_PARENTESES_I  = r'\('
t_PARENTESES_F  = r'\)'
t_CHAVES_I      = r'{'
t_CHAVES_F      = r'}'
t_IGUAL         = r'='
t_AND           = r'&&'
t_OPLOGIC       = r'>=|<=|==|!=|>|<'

def t_BOOL(t):
    r'TRUE|FALSE'
    # Converte para 1 ou 0 para C
    t.value = 1 if t.value == 'TRUE' else 0
    return t

def t_NUM(t):
    r'[0-9]+'
    # O enunciado especifica que são inteiros não negativos 
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"[^\"]*\"'
    # Remove as aspas do valor
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservados.get(t.value, 'ID') # Verifica se é uma palavra reservada
    return t

t_ignore = " \t\n" # Ignorar whitespaces

def t_error(t):
    print("Caracter ilegal: ", t.value[0])
    t.lexer.skip(1)

# Construção do Lexer
lexer = lex(debug=False)

# --- REGRAS DA GRAMÁTICA (YACC) ---

def p_programm(p):
    '''
    PROGRAMM : DEVICES CMDS
    '''
    # Junta as declarações de dispositivos com os comandos
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
    DEVICE : DISPOSITIVO DOIS_PONTOS CHAVES_I ID CHAVES_F
           | DISPOSITIVO DOIS_PONTOS CHAVES_I ID VIRGULA ID CHAVES_F
    '''
    # Gera a declaração de variáveis em C
    if len(p) == 6:
        # dispositivo: {namedevice}
        # O enunciado diz que namedevice só pode conter letras [cite: 14]
        p[0] = f'    char* {p[4]} = "{p[4]}";\n'
    else:
        # dispositivo: {namedevice, observation}
        # Todo valor não definido deve ser zero [cite: 43]
        # Todas as variáveis numéricas são inteiras 
        p[0] = f'    char* {p[4]} = "{p[4]}";\n    int {p[6]} = 0;\n'

def p_cmds(p):
    '''
    CMDS : CMDS CMD_TERMINATED
         | CMD_TERMINATED
    '''
    # Constrói a lista de comandos C
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]
        
def p_cmd_terminated(p):
    '''
    CMD_TERMINATED : CMD DOT
    '''
    # O ponto finaliza o comando, em C isso é um ';'
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
    OBSACT : SE OBS ENTAO ACT
           | SE OBS ENTAO ACT SENAO ACT
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
    # A regra 'num bool' do enunciado foi corrigida conforme a permissão de alteração 
    p[0] = str(p[1])

def p_act(p):
    '''
    ACT : ACTION ID
        | ENVIAR ALERTA PARENTESES_I STRING PARENTESES_F ID
        | ENVIAR ALERTA PARENTESES_I STRING VIRGULA ID PARENTESES_F ID
        | ENVIAR ALERTA PARENTESES_I STRING PARENTESES_F PARA TODOS DOIS_PONTOS NAMEDEVICELIST
    '''
    if len(p) == 3: # Ligar/Desligar
        p[0] = f'{p[1]}({p[2]})'
    elif len(p) == 7: # Alerta simples: enviar alerta ("msg") device
        p[0] = f'alerta({p[6]}, "{p[4]}")'
    elif len(p) == 9 and p[5] == ',': # Alerta com observação: enviar alerta ("msg", obs) device
        p[0] = f'alertaComObs({p[8]}, "{p[4]}", {p[6]})'
    else: # Alerta broadcast: enviar alerta ("msg") para todos: dev1, dev2 ...
        devices = p[8]
        msg = p[4]
        count = len(devices)
        # Cria um array em C com os nomes dos dispositivos
        device_array_str = ", ".join([f'"{d}"' for d in devices])
        p[0] = f'char* broadcast_devices_{p.lineno}[] = {{ {device_array_str} }}; alertaTodos(broadcast_devices_{p.lineno}, "{msg}", {count})'

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

# Construção do Parser
parser = yacc(debug=False)

# --- EXECUÇÃO ---
# Use o arquivo 'teste1.ObsAct' como entrada
try:
    with open('teste1.ObsAct', 'r') as arq:
        conteudo = arq.read()
        resultado = parser.parse(conteudo, lexer=lexer)
        if resultado:
            # Junta o preâmbulo C, as declarações e os comandos
            final_c_code = c_code_preamble[0] + resultado + "\n    return 0;\n}\n"
            
            # Salva o código C final no arquivo de saída 'teste1.c'
            with open('teste1.c', 'w') as arq_c:
                arq_c.write(final_c_code)
            print("Arquivo 'teste1.c' gerado com sucesso.")
        else:
            print("Não foi possível gerar o código C devido a erros de sintaxe.")

except FileNotFoundError:
    print("Erro: O arquivo 'teste1.ObsAct' não foi encontrado.")