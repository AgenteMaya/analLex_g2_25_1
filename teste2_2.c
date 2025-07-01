
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
     printf ("%s\n", msg);
}

void alertaComObs ( char* namedevice , char* msg , int var )
{
    printf("%s recebeu o alerta: \n", namedevice);
    printf ("%s %d\n", msg, var);
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
    char* celular = "celular";
    char* movimento = "movimento";
    char* higr_metro = "higr metro";
    char* umidade = "umidade";
    char* lampada = "lampada";
    char* potencia = "potencia";
    char* Monitor = "Monitor";
    potencia = 100;
    if (umidade < 40) {
        alerta(Monitor, " Ar seco detectado ");
    };
    if (movimento == 0) {
        ligar(lampada);
    } else {
        desligar(lampada);
    };

    return 0;
}
