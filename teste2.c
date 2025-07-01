
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

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

int main(void)
{
    char* celular = "celular";
    float movimento = 0;
    char* higr_metro = "higr metro";
    float umidade = 0;
    char* lampada = "lampada";
    float potencia = 0;
    char* Monitor = "Monitor";
    potencia = 100;
    if (umidade < 40) {
        alerta(Monitor, " Ar seco detectado ");
    };
    if (movimento == 1) {
        ligar(lampada);
    } else {
        desligar(lampada);
    };

    return 0;
}
