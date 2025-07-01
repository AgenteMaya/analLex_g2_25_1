
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
    char* monitor = "monitor";
    char* celular = "celular";
    char* Termometro = "Termometro";
    float temperatura = 0;
    temperatura = 32;
    if (temperatura > 30) {
        char* vetorDeDispositivos1[] = { "monitor", "celular" };
    for (int i = 0; i < 2; i++) { alertaComObs(vetorDeDispositivos1[i], " Temperatura em ", temperatura); };
    };

    return 0;
}
