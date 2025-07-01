
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

void alertaTodos(char* namedevices[], char* msg, int var, int qtd)
{
    if (var == INT_MAX)
    {
        for (int i = 0; i < qtd; i++)
        {
            alerta(namedevices[i], msg);
        }
    }
    else
    {
        for (int i = 0; i < qtd; i++)
        {
            alertaComObs(namedevices[i], msg);
        }
    }
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
    if (movimento == 0) {
        ligar(lampada);
    } else {
        desligar(lampada);
    };

    return 0;
}
