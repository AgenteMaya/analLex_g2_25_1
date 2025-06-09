from ply.lex import lex
from ply.yacc import yacc

file = open("c_file.txt", "w")

file.write(
    """
    #include <stdio.h>
    #include <stdlib.h>
    
    """
)